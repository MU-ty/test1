#!/usr/bin/env python3
"""
AI Analyzer Module
使用Claude API分析提取的网页内容
"""

import requests
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class ActivityAnalyzer:
    """使用Claude分析活动信息"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gpt-4o-mini"  # GitHub Models支持的模型
        self.api_url = "https://models.inference.ai.azure.com/chat/completions"
    
    def analyze(self, text: str, category: str, url: str) -> dict:
        """分析网页内容并提取活动信息"""
        try:
            prompt = self._build_prompt(text, category, url)
            response = self._call_api(prompt)
            
            if response.get('success'):
                data = response.get('data', {})
                return {
                    'success': True,
                    'data': data,
                    'category': category,
                    'url': url
                }
            else:
                return {
                    'success': False,
                    'error': response.get('error', '分析失败')
                }
        except Exception as e:
            logger.error(f"AI分析失败: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _build_prompt(self, text: str, category: str, url: str) -> str:
        """构建Claude提示词"""
        return f"""请分析以下网页内容，提取活动相关的信息。返回JSON格式的数据。

网页链接: {url}
活动分类: {category}

网页内容:
{text[:3000]}

请按以下格式返回JSON (只返回JSON，不要其他内容):
{{
    "title": "活动标题",
    "description": "活动简介(1-2句话)",
    "start_date": "开始日期 (YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS)",
    "end_date": "结束日期 (YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS，如果没有就等于start_date)",
    "location": "地点 (如果是线上活动写'Online')",
    "url": "{url}",
    "tags": ["标签1", "标签2"],
    "registration_url": "报名链接 (如果没有就写null)",
    "is_online": true/false
}}

如果某些字段无法从文本中确定，使用合理的默认值或null。确保返回的JSON格式完整且有效。"""
    
    def _call_api(self, prompt: str) -> dict:
        """调用GitHub Models API"""
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": self.model,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant that extracts structured information from web content. Always respond with valid JSON only, no markdown formatting."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 500,
                "top_p": 1
            }
            
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            message = result.get('choices', [{}])[0].get('message', {}).get('content', '{}')
            
            # 清理markdown格式
            if message.startswith('```json'):
                message = message[7:]
            if message.startswith('```'):
                message = message[3:]
            if message.endswith('```'):
                message = message[:-3]
            message = message.strip()
            
            data = json.loads(message)
            
            # 验证必要字段
            required_fields = ['title', 'description', 'start_date', 'end_date', 'location', 'tags']
            for field in required_fields:
                if field not in data:
                    data[field] = None
            
            return {
                'success': True,
                'data': data
            }
        
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析失败: {str(e)}")
            return {
                'success': False,
                'error': f"JSON解析失败: {str(e)}"
            }
        except requests.exceptions.RequestException as e:
            logger.error(f"API调用失败: {str(e)}")
            return {
                'success': False,
                'error': f"API调用失败: {str(e)}"
            }
        except Exception as e:
            logger.error(f"未知错误: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
