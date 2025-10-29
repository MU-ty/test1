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
    
    # 步骤3：格式化输出（供 Issue 评论显示）
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
    start = data.get('start_date', 'N/A')
    end = data.get('end_date', 'N/A')
    print(f"> {start} to {end}")
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
    print("- Review the extracted information above")
    print("- Reply with feedback if any corrections are needed")
    
    return True

if __name__ == '__main__':
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Fatal error: {str(e)}")
        sys.exit(1)
