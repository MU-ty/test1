#!/usr/bin/env python3
"""
AI-powered Activity Information Extractor
Extracts structured activity data from URLs using GitHub Models API
"""

import json
import os
import sys
import re
from datetime import datetime
from urllib.parse import urlparse
from typing import Dict, List, Optional, Tuple
import base64
import subprocess

import requests
import yaml
from pathlib import Path


class ActivityExtractor:
    """Extracts activity information using Claude Vision via GitHub Models API"""

    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.api_key = os.getenv("GITHUB_MODELS_API_KEY", self.github_token)
        self.activity_url = os.getenv("ACTIVITY_URL")
        self.activity_category = os.getenv("ACTIVITY_CATEGORY", "activity")
        self.issue_number = os.getenv("ISSUE_NUMBER")
        
        # API configuration
        self.model_api_endpoint = "https://models.inference.ai.azure.com/chat/completions"
        self.model_name = "claude-3-5-sonnet"  # GitHub Models 提供的模型
        
        # Data paths
        self.data_dir = Path("data")
        self.existing_tags = self._load_existing_tags()
        self.existing_ids = self._load_existing_ids()

    def _load_existing_tags(self) -> Dict[str, List[str]]:
        """Load existing tags from all YAML files"""
        tags_dict = {}
        for category in ["activities", "conferences", "competitions"]:
            file_path = self.data_dir / f"{category}.yml"
            tags_dict[category] = []
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or []
                        for item in data:
                            if isinstance(item, dict) and 'tags' in item:
                                tags_dict[category].extend(item['tags'])
                    # Remove duplicates
                    tags_dict[category] = list(set(tags_dict[category]))
                except Exception as e:
                    print(f"Warning: Failed to load tags from {file_path}: {e}")
        
        return tags_dict

    def _load_existing_ids(self) -> set:
        """Load all existing event IDs to ensure uniqueness"""
        existing_ids = set()
        for category in ["activities", "conferences", "competitions"]:
            file_path = self.data_dir / f"{category}.yml"
            
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = yaml.safe_load(f) or []
                        for item in data:
                            if isinstance(item, dict) and 'events' in item:
                                for event in item['events']:
                                    if isinstance(event, dict) and 'id' in event:
                                        existing_ids.add(event['id'])
                except Exception as e:
                    print(f"Warning: Failed to load IDs from {file_path}: {e}")
        
        return existing_ids

    def _fetch_webpage_content(self, url: str) -> Optional[str]:
        """
        Fetch webpage content from URL
        Returns HTML content or None if failed
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url}: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching {url}: {str(e)}")
            return None

    def _extract_text_from_html(self, html: str) -> str:
        """Extract text content from HTML, removing scripts and styles"""
        try:
            from html.parser import HTMLParser
            import re
            
            # Remove script and style tags
            html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
            html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL)
            
            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '\n', html)
            
            # Clean up whitespace
            text = re.sub(r'\n+', '\n', text)
            text = re.sub(r' +', ' ', text)
            
            return text.strip()
        except Exception as e:
            print(f"Error extracting text from HTML: {e}")
            return ""

    def _call_claude_vision_api(self, content: str, instruction: str) -> Optional[Dict]:
        """Call Claude 3.5 Vision API via GitHub Models"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # Prepare message with text content
            message_content = [
                {
                    "type": "text",
                    "text": f"{instruction}\n\n相关网页内容（前2000字）:\n\n{content[:2000]}"
                }
            ]
            
            payload = {
                "model": self.model_name,
                "messages": [
                    {
                        "role": "user",
                        "content": message_content
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 1000
            }
            
            response = requests.post(
                self.model_api_endpoint,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get("choices") and len(result["choices"]) > 0:
                    return {
                        "success": True,
                        "content": result["choices"][0]["message"]["content"]
                    }
                else:
                    return {"success": False, "error": "Empty response from API"}
            else:
                error_msg = response.text
                print(f"API Error: {response.status_code} - {error_msg}")
                return {"success": False, "error": f"API returned {response.status_code}"}
                
        except Exception as e:
            print(f"Error calling Claude API: {str(e)}")
            return {"success": False, "error": str(e)}

    def _parse_claude_response(self, response_text: str) -> Optional[Dict]:
        """Parse Claude's response to extract structured activity data"""
        try:
            # Try to extract JSON from code blocks or direct JSON
            json_pattern = r'```(?:json)?\s*(\{.*?\})\s*```'
            json_match = re.search(json_pattern, response_text, re.DOTALL)
            
            if json_match:
                json_str = json_match.group(1)
            else:
                # Try direct JSON parsing
                json_str = response_text
            
            # Parse JSON
            data = json.loads(json_str)
            return data
            
        except json.JSONDecodeError as e:
            print(f"Failed to parse Claude response as JSON: {e}")
            print(f"Response text: {response_text[:500]}")
            return None

    def _generate_event_id(self, title: str, year: int) -> str:
        """Generate a unique event ID from title and year"""
        # Convert to pinyin-compatible slug
        slug = re.sub(r'[^\w\s-]', '', title.lower())
        slug = re.sub(r'[-\s]+', '-', slug).strip('-')
        
        base_id = f"{slug}{year}"
        event_id = base_id
        counter = 1
        
        # Ensure uniqueness
        while event_id in self.existing_ids:
            event_id = f"{base_id}-{counter}"
            counter += 1
        
        self.existing_ids.add(event_id)
        return event_id

    def _normalize_tags(self, tags: List[str], category: str) -> Tuple[List[str], str]:
        """
        Normalize tags and check for duplicates
        Returns (normalized_tags, validation_info)
        """
        existing_tags = self.existing_tags.get(category.replace('.yml', ''), [])
        normalized = []
        duplicates = []
        new_tags = []
        
        for tag in tags:
            tag = tag.strip()
            
            # Check if similar tag already exists (case-insensitive)
            existing_match = next(
                (t for t in existing_tags if t.lower() == tag.lower()),
                None
            )
            
            if existing_match:
                normalized.append(existing_match)
                if existing_match not in duplicates:
                    duplicates.append(existing_match)
            else:
                normalized.append(tag)
                if tag not in new_tags:
                    new_tags.append(tag)
        
        # Remove duplicates from normalized list
        normalized = list(dict.fromkeys(normalized))
        
        info = ""
        if duplicates:
            info += f"✅ 复用现有标签: {', '.join(duplicates)}\n"
        if new_tags:
            info += f"✨ 新建标签: {', '.join(new_tags)}"
        
        return normalized, info.strip()

    def extract(self) -> Dict:
        """Main extraction workflow"""
        if not self.activity_url:
            return {
                "success": False,
                "error": "未提供活动URL。请使用以下格式: @activity-bot extract https://example.com"
            }
        
        print(f"[*] 开始提取活动信息: {self.activity_url}")
        
        # Step 1: Fetch webpage content
        print("[*] 正在获取网页内容...")
        html_content = self._fetch_webpage_content(self.activity_url)
        if not html_content:
            return {
                "success": False,
                "error": f"无法访问提供的URL: {self.activity_url}\n请确保URL有效且网站可访问。"
            }
        
        # Step 2: Extract text from HTML
        print("[*] 正在提取文本...")
        text_content = self._extract_text_from_html(html_content)
        if len(text_content) < 100:
            return {
                "success": False,
                "error": "网页内容过少，无法提取有效信息。请确保URL指向包含活动详情的页面。"
            }
        
        # Step 3: Call Claude to extract structured data
        print("[*] 使用AI模型分析活动信息...")
        
        extraction_prompt = f"""请从以下网页内容中提取开源活动的结构化信息，并返回JSON格式。

必须包含的字段:
- title: 活动名称 (字符串)
- description: 一句话活动描述，不超过100字 (字符串)
- tags: 标签列表，最多5个 (数组)
- year: 年份 (整数，如2025)
- link: 活动链接 (字符串)
- timeline: 关键日期列表，每个包含deadline和comment (数组)
- timezone: 时区，使用IANA标准，默认Asia/Shanghai (字符串)
- date: 人类可读的日期范围，如"2025年4月30日"或"2025年4月30日-9月30日" (字符串)
- place: 地点，格式如"线上"或"国家，城市" (字符串)

返回格式:
```json
{{
  "title": "...",
  "description": "...",
  "tags": ["...", "..."],
  "year": 2025,
  "link": "...",
  "timeline": [
    {{"deadline": "2025-01-01T00:00:00", "comment": "..."}},
    ...
  ],
  "timezone": "Asia/Shanghai",
  "date": "2025年1月1日",
  "place": "线上"
}}
```

重要提示:
1. deadline必须是ISO 8601格式: YYYY-MM-DDTHH:mm:ss
2. 如果无法确定具体时间，使用00:00:00
3. 如果无法找到某个字段，使用null
4. 标签应该简洁明了，避免冗余"""

        api_response = self._call_claude_vision_api(text_content, extraction_prompt)
        
        if not api_response.get("success"):
            return {
                "success": False,
                "error": f"AI分析失败: {api_response.get('error', '未知错误')}\n\n"
                         f"建议:\n"
                         f"1. 检查网络连接\n"
                         f"2. 尝试不同的活动URL\n"
                         f"3. 或在issue中直接粘贴活动详情"
            }
        
        # Parse response
        extracted_data = self._parse_claude_response(api_response.get("content", ""))
        if not extracted_data:
            return {
                "success": False,
                "error": "无法解析AI响应，格式不正确"
            }
        
        # Step 4: Validation and normalization
        print("[*] 验证并规范化数据...")
        
        # Generate unique ID
        event_id = self._generate_event_id(
            extracted_data.get("title", "event"),
            extracted_data.get("year", 2025)
        )
        
        # Normalize tags
        category_name = f"{self.activity_category}s"  # activities, conferences, competitions
        normalized_tags, tags_info = self._normalize_tags(
            extracted_data.get("tags", []),
            category_name
        )
        
        # Step 5: Build YAML entry
        print("[*] 生成YAML格式...")
        
        yaml_data = {
            "title": extracted_data.get("title", "Unknown"),
            "description": extracted_data.get("description", ""),
            "category": self.activity_category,
            "tags": normalized_tags,
            "events": [
                {
                    "year": extracted_data.get("year", 2025),
                    "id": event_id,
                    "link": extracted_data.get("link", self.activity_url),
                    "timeline": extracted_data.get("timeline", []),
                    "timezone": extracted_data.get("timezone", "Asia/Shanghai"),
                    "date": extracted_data.get("date", ""),
                    "place": extracted_data.get("place", "线上")
                }
            ]
        }
        
        # Convert to YAML string
        yaml_content = yaml.dump([yaml_data], allow_unicode=True, default_flow_style=False)
        
        # Check ID uniqueness
        id_unique = event_id not in self.existing_ids
        
        print("[+] 提取完成！")
        
        return {
            "success": True,
            "yaml_content": yaml_content,
            "category": self.activity_category,
            "validation": {
                "id_unique": id_unique,
                "event_id": event_id,
                "tags_info": tags_info,
                "extracted_data": extracted_data
            },
            "issue_number": self.issue_number
        }


def main():
    """Main entry point"""
    extractor = ActivityExtractor()
    result = extractor.extract()
    
    # Save results to file for GitHub Actions
    with open("ai-bot-results.json", "w", encoding="utf-8") as f:
        # Convert result to be JSON serializable
        serializable_result = {
            "success": result.get("success"),
            "yaml_content": result.get("yaml_content", ""),
            "category": result.get("category", ""),
            "error": result.get("error", ""),
            "validation": {
                "id_unique": result.get("validation", {}).get("id_unique", False),
                "tags_info": result.get("validation", {}).get("tags_info", "")
            }
        }
        json.dump(serializable_result, f, ensure_ascii=False, indent=2)
    
    # Print results
    if result.get("success"):
        print("\n" + "="*50)
        print("✅ 提取成功")
        print("="*50)
        print(result.get("yaml_content"))
        print("="*50)
    else:
        print("\n" + "="*50)
        print("❌ 提取失败")
        print("="*50)
        print(result.get("error", "未知错误"))
        print("="*50)
    
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
