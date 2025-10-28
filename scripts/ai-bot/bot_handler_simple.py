#!/usr/bin/env python3
"""
AI Bot Handler - Simplified Test Version
测试版本，用于验证基本功能
"""

import os
import sys
import json
import logging
from datetime import datetime

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("=" * 60)
    logger.info("AI Bot Handler - Started")
    logger.info("=" * 60)
    
    # 第1步：检查环境变量
    logger.info("\n[Step 1] Checking environment variables...")
    
    token = os.getenv('GITHUB_TOKEN')
    models_token = os.getenv('GH_MODELS_TOKEN')
    repo = os.getenv('GITHUB_REPOSITORY')
    issue = os.getenv('GITHUB_ISSUE_NUMBER')
    url = os.getenv('BOT_URL')
    category = os.getenv('BOT_CATEGORY', 'activity')
    
    logger.info(f"GITHUB_TOKEN: {'✓ Set' if token else '✗ Missing'}")
    logger.info(f"GH_MODELS_TOKEN: {'✓ Set' if models_token else '✗ Missing'}")
    logger.info(f"GITHUB_REPOSITORY: {repo}")
    logger.info(f"GITHUB_ISSUE_NUMBER: {issue}")
    logger.info(f"BOT_URL: {url}")
    logger.info(f"BOT_CATEGORY: {category}")
    
    if not models_token:
        logger.error("\n❌ GH_MODELS_TOKEN is not set!")
        logger.error("Please configure GH_MODELS_TOKEN in GitHub Secrets")
        return False
    
    if not url:
        logger.error("\n❌ BOT_URL is not set!")
        logger.error("No URL provided in command")
        return False
    
    # 第2步：尝试爬取网页
    logger.info("\n[Step 2] Attempting to scrape webpage...")
    
    try:
        from web_scraper import WebScraper
        
        scraper = WebScraper()
        logger.info(f"Scraping: {url}")
        result = scraper.scrape(url)
        
        if result['success']:
            logger.info(f"✓ Success! Got {len(result['text'])} characters")
            logger.info(f"  Metadata: {result['metadata']}")
        else:
            logger.error(f"✗ Failed: {result['error']}")
            print(f"\n❌ **Failed to scrape webpage**\n\nError: {result['error']}\n\nURL: {url}")
            return False
    
    except Exception as e:
        logger.error(f"✗ Exception: {e}")
        print(f"\n❌ **Exception during scraping**\n\nError: {str(e)}\n\nPlease check the logs.")
        return False
    
    # 第3步：尝试AI分析
    logger.info("\n[Step 3] Attempting AI analysis...")
    
    try:
        from ai_analyzer import ActivityAnalyzer
        
        analyzer = ActivityAnalyzer(models_token)
        logger.info("Calling Claude AI...")
        
        analysis = analyzer.analyze(
            text=result['text'],
            category=category,
            url=url
        )
        
        if analysis['success']:
            logger.info(f"✓ AI Analysis successful!")
            data = analysis['data']
            logger.info(f"  Title: {data.get('title', 'N/A')}")
            logger.info(f"  Tags: {data.get('tags', [])}")
            
            # 输出成功消息
            message = f"""
✅ **Activity Extracted Successfully!**

📌 **Title**: {data.get('title', 'N/A')}

📝 **Description**: {data.get('description', 'N/A')[:200]}

🗓️ **Date**: {data.get('start_date', 'N/A')} ~ {data.get('end_date', 'N/A')}

📍 **Location**: {data.get('location', 'N/A')}

🏷️ **Tags**: {', '.join(data.get('tags', []))}

🔗 **Source**: {data.get('url', 'N/A')}

---

Next step: Reply with `@activity-bot confirm` to create a PR
"""
            print(message)
            return True
        else:
            logger.error(f"✗ AI analysis failed: {analysis['error']}")
            print(f"\n❌ **AI Analysis Failed**\n\nError: {analysis['error']}")
            return False
    
    except Exception as e:
        logger.error(f"✗ Exception: {e}", exc_info=True)
        print(f"\n❌ **Exception during AI analysis**\n\nError: {str(e)}\n\nPlease check the logs.")
        return False

if __name__ == '__main__':
    try:
        success = main()
        logger.info("\n" + "=" * 60)
        if success:
            logger.info("✓ Completed successfully")
        else:
            logger.error("✗ Failed")
        logger.info("=" * 60)
        
        sys.exit(0 if success else 1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
