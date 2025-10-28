#!/usr/bin/env python3
"""
Data Validator Module
验证提取的活动数据是否符合要求
"""

import yaml
import logging
from datetime import datetime
from pathlib import Path

logger = logging.getLogger(__name__)


class DataValidator:
    """数据验证类"""
    
    def __init__(self, data_dir: str = 'data'):
        self.data_dir = Path(data_dir)
        self.existing_ids = set()
        self._load_existing_ids()
    
    def _load_existing_ids(self):
        """加载现有的活动ID"""
        try:
            for file in self.data_dir.glob('*.yml'):
                with open(file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or []
                    if isinstance(data, list):
                        for item in data:
                            if isinstance(item, dict) and 'id' in item:
                                self.existing_ids.add(item['id'])
        except Exception as e:
            logger.warning(f"加载现有ID失败: {str(e)}")
    
    def validate(self, data: dict, category: str) -> dict:
        """验证完整的活动数据"""
        try:
            errors = []
            warnings = []
            
            # 检查必要字段
            required_fields = ['title', 'description', 'start_date', 'location', 'tags']
            for field in required_fields:
                if not data.get(field):
                    errors.append(f"缺少必要字段: {field}")
            
            # 检查标题长度
            if data.get('title'):
                if len(data['title']) < 5:
                    errors.append("标题过短 (最少5个字符)")
                elif len(data['title']) > 200:
                    warnings.append("标题过长 (建议不超过200个字符)")
            
            # 检查描述长度
            if data.get('description'):
                if len(data['description']) < 10:
                    errors.append("描述过短 (最少10个字符)")
                elif len(data['description']) > 1000:
                    warnings.append("描述过长 (建议不超过1000个字符)")
            
            # 检查日期格式
            start_date_valid = self._validate_date(data.get('start_date'))
            if not start_date_valid:
                errors.append(f"开始日期格式无效: {data.get('start_date')}")
            
            end_date = data.get('end_date', data.get('start_date'))
            end_date_valid = self._validate_date(end_date)
            if not end_date_valid:
                errors.append(f"结束日期格式无效: {end_date}")
            
            # 检查日期逻辑
            if start_date_valid and end_date_valid:
                try:
                    start = self._parse_date(data.get('start_date'))
                    end = self._parse_date(end_date)
                    if end < start:
                        errors.append("结束日期不能早于开始日期")
                except:
                    pass
            
            # 检查标签
            tags = data.get('tags', [])
            if not isinstance(tags, list):
                errors.append("标签必须是列表")
            elif len(tags) == 0:
                errors.append("至少需要一个标签")
            elif len(tags) > 10:
                warnings.append("标签过多 (建议不超过10个)")
            
            # 检查位置
            location = data.get('location', '')
            if isinstance(location, str):
                if location.lower() != 'online' and len(location) < 2:
                    errors.append("地点信息过短")
            
            return {
                'valid': len(errors) == 0,
                'errors': errors,
                'warnings': warnings
            }
        
        except Exception as e:
            logger.error(f"数据验证异常: {str(e)}")
            return {
                'valid': False,
                'errors': [f"验证过程出错: {str(e)}"],
                'warnings': []
            }
    
    def _validate_date(self, date_str: str) -> bool:
        """验证日期格式"""
        if not date_str:
            return False
        
        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
            try:
                datetime.strptime(date_str, fmt)
                return True
            except ValueError:
                continue
        
        return False
    
    def _parse_date(self, date_str: str) -> datetime:
        """解析日期字符串"""
        for fmt in ['%Y-%m-%d', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        
        raise ValueError(f"无法解析日期: {date_str}")
    
    def check_id_conflict(self, activity_id: str) -> bool:
        """检查ID是否已存在"""
        return activity_id in self.existing_ids
    
    def normalize_tags(self, tags: list) -> list:
        """标准化标签"""
        if not isinstance(tags, list):
            return []
        
        # 转换为小写并去重
        normalized = []
        seen = set()
        
        for tag in tags:
            if isinstance(tag, str):
                normalized_tag = tag.strip().lower()
                if normalized_tag and normalized_tag not in seen:
                    normalized.append(normalized_tag)
                    seen.add(normalized_tag)
        
        return normalized
