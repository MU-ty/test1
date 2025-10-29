#!/usr/bin/env python3
"""
AI Bot Handler - Simplified Version
输出格式优化以适配 GitHub Issue 评论
"""

import os
import sys
import json

# 确保输出实时刷新
sys.stdout = open(sys.stdout.fileno(), mode='w', buffering=1, encoding='utf-8')
sys.stderr = open(sys.stderr.fileno(), mode='w', buffering=1, encoding='utf-8')

# 禁用日志以保持输出清洁
import logging
logging.disable(logging.CRITICAL)

def main():
    # 获取环境变量
    url = os.getenv('BOT_URL')
    category = os.getenv('BOT_CATEGORY', 'activity')
    models_token = os.getenv('GH_MODELS_TOKEN')
    
    if not url:
        print("❌ No URL provided")
        return False
    
    if not models_token:
        print("❌ GH_MODELS_TOKEN not configured")
        return False
    
    # 步骤1：爬取网页
    try:
        from web_scraper import WebScraper
        scraper = WebScraper()
        result = scraper.scrape(url)
        
        if not result['success']:
            print(f"❌ Failed to scrape: {result['error']}")
            return False
        
        scraped_text = result['text']
        metadata = result['metadata']
    
    except Exception as e:
        print(f"❌ Scraping error: {str(e)}")
        return False
    
    # 步骤2：AI分析
    try:
        from ai_analyzer import ActivityAnalyzer
        analyzer = ActivityAnalyzer(models_token)
        analysis = analyzer.analyze(
            text=scraped_text,
            category=category,
            url=url
        )
        
        if not analysis['success']:
            print(f"❌ AI analysis failed: {analysis['error']}")
            return False
        
        data = analysis['data']
    
    except Exception as e:
        print(f"❌ AI error: {str(e)}")
        return False
    
    # 步骤3：保存提取的数据为JSON（用于 PR 创建工作流）
    activity_json = json.dumps({
        'title': data.get('title', 'Untitled'),
        'description': data.get('description', ''),
        'start_date': data.get('start_date', ''),
        'end_date': data.get('end_date', ''),
        'location': data.get('location', 'Online'),
        'url': url,
        'tags': data.get('tags', []),
        'registration_url': data.get('registration_url'),
        'is_online': data.get('is_online', False),
        'category': category
    }, ensure_ascii=False)
    
    # 不输出 JSON，防止乱码。改为输出到 stderr 用于调试
    import sys as sys_module
    sys_module.stderr.write(f"DEBUG: Activity JSON: {activity_json}\n")
    
    # 步骤4：格式化输出（供 Issue 评论显示）
    print("✅ **Activity Extracted Successfully!**")
    print("")
    print("📌 **Title**")
    print(f"> {data.get('title', 'N/A')}")
    print("")
    print("📝 **Description**")
    desc = data.get('description', 'N/A')
    if desc and desc != 'N/A':
        print(f"> {desc[:200]}")
    else:
        print("> No description available")
    print("")
    print("🗓️ **Date**")
    start = data.get('start_date')
    end = data.get('end_date')
    
    # 处理日期为 None 或 null 的情况
    if start and start not in ['None', 'null', None]:
        if end and end not in ['None', 'null', None] and end != start:
            print(f"> {start} to {end}")
        else:
            print(f"> {start}")
    else:
        print("> Date not specified in the event page")
    print("")
    print("📍 **Location**")
    loc = data.get('location', 'N/A')
    if loc and loc not in ['N/A', 'null']:
        print(f"> {loc}")
    else:
        print("> Online")
    print("")
    print("🏷️ **Tags**")
    tags = data.get('tags', [])
    if tags:
        tags_str = ", ".join(tags)
        print(f"> {tags_str}")
    else:
        print("> No tags")
    print("")
    print("🔗 **Source**")
    print(f"> {url}")
    print("")
    print("---")
    print("")
    print("✨ **Next Steps:**")
    print("- Verify the extracted information above is accurate")
    print("- A PR will be automatically created to add this activity to the data files")
    print("- Please review and merge when ready")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)
