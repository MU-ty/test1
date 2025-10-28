#!/usr/bin/env python3
"""
AI Bot Handler - Main Script
处理@activity-bot命令并执行相应操作
"""

import sys
import os
import json
import yaml
import logging
from pathlib import Path
from datetime import datetime

# 添加scripts目录到Python路径
sys.path.insert(0, str(Path(__file__).parent))

from web_scraper import WebScraper
from ai_analyzer import ActivityAnalyzer
from data_validator import DataValidator
from utils import setup_logging, load_github_context, generate_activity_id, save_json, load_json

# 设置日志
logger = setup_logging(__name__)


def handle_extract_command():
    """处理extract命令 - 从URL提取活动信息"""
    
    logger.info("开始处理extract命令...")
    
    # 获取环境变量
    url = os.getenv('BOT_URL')
    category = os.getenv('BOT_CATEGORY', 'activity')
    issue_number = os.getenv('BOT_ISSUE')
    repo_path = os.getenv('GITHUB_WORKSPACE', '.')
    api_key = os.getenv('GH_MODELS_TOKEN')
    
    if not url:
        logger.error("缺少BOT_URL环境变量")
        return save_error("缺少URL参数", issue_number)
    
    if not api_key:
        logger.error("缺少GH_MODELS_TOKEN环境变量")
        return save_error("缺少API密钥配置", issue_number)
    
    logger.info(f"目标URL: {url}, 类别: {category}")
    
    try:
        # Step 1: 爬取网页
        logger.info("Step 1: 爬取网页内容...")
        scraper = WebScraper()
        scrape_result = scraper.scrape(url)
        
        if not scrape_result['success']:
            error_msg = f"网页爬取失败: {scrape_result.get('error', '未知错误')}"
            logger.error(error_msg)
            return save_error(error_msg, issue_number)
        
        text = scrape_result['text']
        logger.info(f"✓ 成功爬取 {len(text)} 字符的内容")
        
        # Step 2: 使用Claude AI分析
        logger.info("Step 2: 使用Claude分析内容...")
        analyzer = ActivityAnalyzer(api_key)
        analysis_result = analyzer.analyze(text, category, url)
        
        if not analysis_result['success']:
            error_msg = f"AI分析失败: {analysis_result.get('error', '未知错误')}"
            logger.error(error_msg)
            return save_error(error_msg, issue_number)
        
        activity_data = analysis_result['data']
        logger.info(f"✓ 成功分析，标题: {activity_data.get('title')}")
        
        # Step 3: 数据验证
        logger.info("Step 3: 验证数据...")
        validator = DataValidator(os.path.join(repo_path, 'data'))
        validation_result = validator.validate(activity_data, category)
        
        if not validation_result['valid']:
            errors = '\n'.join(validation_result['errors'])
            error_msg = f"数据验证失败:\n{errors}"
            logger.error(error_msg)
            return save_error(error_msg, issue_number)
        
        if validation_result['warnings']:
            logger.warning(f"警告: {validation_result['warnings']}")
        
        logger.info("✓ 数据验证通过")
        
        # Step 4: 生成YAML
        logger.info("Step 4: 生成YAML...")
        activity_data['id'] = generate_activity_id(activity_data['title'], activity_data.get('start_date', ''))
        activity_data['tags'] = validator.normalize_tags(activity_data.get('tags', []))
        
        # 检查ID重复
        if validator.check_id_conflict(activity_data['id']):
            # 添加时间戳避免重复
            activity_data['id'] = f"{activity_data['id']}-{datetime.now().strftime('%s')[-6:]}"
        
        yaml_data = yaml.dump([activity_data], allow_unicode=True, default_flow_style=False)
        logger.info("✓ YAML生成完成")
        
        # Step 5: 保存结果
        logger.info("Step 5: 保存结果...")
        result = {
            'success': True,
            'activity_id': activity_data['id'],
            'category': category,
            'url': url,
            'yaml': yaml_data,
            'data': activity_data,
            'timestamp': datetime.now().isoformat()
        }
        
        return save_result(result, issue_number)
        
    except Exception as e:
        error_msg = f"处理过程中出现异常: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return save_error(error_msg, issue_number)


def handle_confirm_command():
    """处理confirm命令 - 确认之前的提取结果"""
    
    logger.info("开始处理confirm命令...")
    
    # 获取环境变量
    issue_number = os.getenv('BOT_ISSUE')
    repo_path = os.getenv('GITHUB_WORKSPACE', '.')
    
    try:
        # 加载之前的结果
        result_file = os.path.join(repo_path, f'.bot-result-{issue_number}.json')
        
        if not os.path.exists(result_file):
            error_msg = "找不到之前的提取结果，请先运行extract命令"
            logger.error(error_msg)
            return save_error(error_msg, issue_number)
        
        with open(result_file, 'r', encoding='utf-8') as f:
            previous_result = json.load(f)
        
        if not previous_result.get('success'):
            error_msg = "之前的提取失败，无法确认"
            logger.error(error_msg)
            return save_error(error_msg, issue_number)
        
        logger.info(f"✓ 已加载之前的结果: {previous_result.get('activity_id')}")
        
        # 标记为已确认
        result = {
            'success': True,
            'confirmed': True,
            'activity_id': previous_result.get('activity_id'),
            'category': previous_result.get('category'),
            'yaml': previous_result.get('yaml'),
            'data': previous_result.get('data'),
            'timestamp': datetime.now().isoformat()
        }
        
        return save_result(result, issue_number)
        
    except Exception as e:
        error_msg = f"处理过程中出现异常: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return save_error(error_msg, issue_number)


def generate_yaml(activity_data: dict) -> str:
    """将活动数据转换为YAML格式"""
    try:
        yaml_str = yaml.dump([activity_data], allow_unicode=True, default_flow_style=False)
        return yaml_str
    except Exception as e:
        logger.error(f"YAML生成失败: {str(e)}")
        return ""


def save_result(result: dict, issue_number: str = None) -> bool:
    """保存成功的结果"""
    try:
        output_file = f".bot-result-{issue_number}.json" if issue_number else ".bot-result.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        logger.info(f"结果已保存到 {output_file}")
        print(json.dumps(result, ensure_ascii=False))  # 用于GitHub Actions输出
        return True
        
    except Exception as e:
        logger.error(f"保存结果失败: {str(e)}")
        return False


def save_error(error_msg: str, issue_number: str = None) -> bool:
    """保存错误信息"""
    try:
        output_file = f".bot-result-{issue_number}.json" if issue_number else ".bot-result.json"
        
        error_result = {
            'success': False,
            'error': error_msg,
            'timestamp': datetime.now().isoformat()
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(error_result, f, ensure_ascii=False, indent=2)
        
        logger.error(f"错误已记录到 {output_file}")
        print(json.dumps(error_result, ensure_ascii=False))  # 用于GitHub Actions输出
        return False
        
    except Exception as e:
        logger.error(f"保存错误失败: {str(e)}")
        return False


def main():
    """主入口"""
    logger.info("AI Bot Handler 启动")
    
    # 获取命令
    command = sys.argv[1] if len(sys.argv) > 1 else None
    
    if command == 'extract':
        handle_extract_command()
    elif command == 'confirm':
        handle_confirm_command()
    else:
        logger.error(f"未知的命令: {command}")
        logger.info("支持的命令: extract, confirm")
        sys.exit(1)


if __name__ == '__main__':
    main()
