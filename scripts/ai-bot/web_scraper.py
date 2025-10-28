#!/usr/bin/env python3
"""
Web Scraper Module
使用requests和BeautifulSoup爬取网页内容
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)


class WebScraper:
    """网页爬虫类"""
    
    def __init__(self, timeout=10, max_retries=3):
        self.timeout = timeout
        self.max_retries = max_retries
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def scrape(self, url: str) -> dict:
        """完整的爬取流程"""
        try:
            html = self.fetch_page(url)
            text = self.extract_text(html)
            metadata = self.extract_metadata(html, url)
            
            if len(text) < 50:
                return {
                    'success': False,
                    'url': url,
                    'error': '网页内容过少，无法提取有效信息'
                }
            
            return {
                'success': True,
                'url': url,
                'text': text[:5000],  # 限制文本长度
                'metadata': metadata,
                'html': html
            }
        except Exception as e:
            logger.error(f"爬取失败 {url}: {str(e)}")
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
    
    def fetch_page(self, url: str) -> str:
        """获取网页HTML"""
        for attempt in range(self.max_retries):
            try:
                response = self.session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True
                )
                response.raise_for_status()
                response.encoding = response.apparent_encoding or 'utf-8'
                return response.text
            except requests.exceptions.RequestException as e:
                logger.warning(f"尝试 {attempt + 1}/{self.max_retries} 失败: {str(e)}")
                if attempt == self.max_retries - 1:
                    raise
        
        raise Exception("网页爬取失败")
    
    def extract_text(self, html: str) -> str:
        """从HTML中提取文本"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # 移除script和style标签
            for script in soup(['script', 'style']):
                script.decompose()
            
            # 提取文本
            text = soup.get_text(separator='\n', strip=True)
            
            # 清理多余空行
            lines = [line.strip() for line in text.split('\n') if line.strip()]
            return '\n'.join(lines)
        except Exception as e:
            logger.warning(f"文本提取失败: {str(e)}")
            return ""
    
    def extract_metadata(self, html: str, url: str) -> dict:
        """提取元数据"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            metadata = {
                'title': '',
                'description': '',
                'keywords': '',
                'domain': urlparse(url).netloc
            }
            
            # 提取标题
            title_tag = soup.find('title')
            if title_tag:
                metadata['title'] = title_tag.get_text(strip=True)
            
            # 提取meta描述
            meta_desc = soup.find('meta', attrs={'name': 'description'})
            if meta_desc:
                metadata['description'] = meta_desc.get('content', '')
            
            # 提取keywords
            meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
            if meta_keywords:
                metadata['keywords'] = meta_keywords.get('content', '')
            
            return metadata
        except Exception as e:
            logger.warning(f"元数据提取失败: {str(e)}")
            return {'title': '', 'description': '', 'keywords': '', 'domain': urlparse(url).netloc}
