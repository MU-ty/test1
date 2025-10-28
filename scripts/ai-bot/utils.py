#!/usr/bin/env python3
"""
Utils Module
共享的工具函数和配置
"""

import logging
import json
import os
from datetime import datetime


def setup_logging(log_file: str = None) -> logging.Logger:
    """设置日志"""
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # 文件输出
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"无法创建日志文件 {log_file}: {str(e)}")
    
    return logger


def load_github_context() -> dict:
    """从GitHub Actions环境加载上下文"""
    context = {
        'event_name': os.getenv('GITHUB_EVENT_NAME', ''),
        'workflow': os.getenv('GITHUB_WORKFLOW', ''),
        'run_id': os.getenv('GITHUB_RUN_ID', ''),
        'run_number': os.getenv('GITHUB_RUN_NUMBER', ''),
        'actor': os.getenv('GITHUB_ACTOR', ''),
        'repository': os.getenv('GITHUB_REPOSITORY', ''),
        'ref': os.getenv('GITHUB_REF', ''),
        'sha': os.getenv('GITHUB_SHA', ''),
        'workspace': os.getenv('GITHUB_WORKSPACE', ''),
        'token': os.getenv('GITHUB_TOKEN', ''),
    }
    
    return context


def generate_activity_id(title: str, start_date: str) -> str:
    """生成活动ID"""
    # 从标题中取前3个单词
    title_part = '-'.join(title.split()[:3]).lower()
    # 从日期中取年月
    try:
        date_part = start_date[:7].replace('-', '')
    except:
        date_part = datetime.now().strftime('%Y%m')
    
    # 生成ID
    activity_id = f"{title_part}-{date_part}"
    # 移除非字母数字字符
    activity_id = ''.join(c if c.isalnum() or c == '-' else '' for c in activity_id)
    # 最多32个字符
    activity_id = activity_id[:32]
    
    return activity_id


def save_json(data: dict, file_path: str) -> bool:
    """保存JSON文件"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        logging.error(f"保存JSON失败 {file_path}: {str(e)}")
        return False


def load_json(file_path: str) -> dict:
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"加载JSON失败 {file_path}: {str(e)}")
        return {}


def sanitize_filename(filename: str) -> str:
    """清理文件名"""
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '')
    return filename[:255]
