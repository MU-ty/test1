#!/usr/bin/env python3
"""
Diagnostic test script - 测试各个组件是否工作
"""

import os
import sys

print("=" * 60)
print("AI Bot Diagnostic Test")
print("=" * 60)

# 测试 1: 环境变量
print("\n[Test 1] Environment Variables")
print("-" * 40)

url = os.getenv('BOT_URL', 'https://competition.atomgit.com/competition')
models_token = os.getenv('GH_MODELS_TOKEN')
github_token = os.getenv('GITHUB_TOKEN')

print(f"BOT_URL: {url}")
print(f"GH_MODELS_TOKEN: {'✓ Set' if models_token else '✗ Missing'}")
print(f"GITHUB_TOKEN: {'✓ Set' if github_token else '✗ Missing'}")

# 测试 2: Web Scraper
print("\n[Test 2] Web Scraper")
print("-" * 40)

try:
    from web_scraper import WebScraper
    scraper = WebScraper()
    print(f"Scraping {url}...")
    result = scraper.scrape(url)
    
    if result['success']:
        print(f"✓ Success! Got {len(result['text'])} characters")
        print(f"  Metadata: {result['metadata']}")
        print(f"  First 200 chars: {result['text'][:200]}")
        scraped_content = result['text']
    else:
        print(f"✗ Failed: {result['error']}")
        scraped_content = None
except Exception as e:
    print(f"✗ Exception: {e}")
    import traceback
    traceback.print_exc()
    scraped_content = None

# 测试 3: AI Analyzer
if scraped_content and models_token:
    print("\n[Test 3] AI Analyzer")
    print("-" * 40)
    
    try:
        from ai_analyzer import ActivityAnalyzer
        analyzer = ActivityAnalyzer(models_token)
        print("Calling AI analyzer...")
        
        analysis = analyzer.analyze(
            text=scraped_content,
            category='competition',
            url=url
        )
        
        if analysis['success']:
            print("✓ AI Analysis successful!")
            data = analysis['data']
            print(f"  Title: {data.get('title', 'N/A')}")
            print(f"  Description: {data.get('description', 'N/A')[:100]}")
            print(f"  Start Date: {data.get('start_date', 'N/A')}")
            print(f"  Tags: {data.get('tags', [])}")
        else:
            print(f"✗ Analysis failed: {analysis['error']}")
    
    except Exception as e:
        print(f"✗ Exception: {e}")
        import traceback
        traceback.print_exc()
else:
    if not scraped_content:
        print("\n[Test 3] AI Analyzer - SKIPPED (no scraped content)")
    if not models_token:
        print("\n[Test 3] AI Analyzer - SKIPPED (no GH_MODELS_TOKEN)")

print("\n" + "=" * 60)
print("Diagnostic Complete")
print("=" * 60)
