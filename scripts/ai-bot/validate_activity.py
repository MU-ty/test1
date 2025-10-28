#!/usr/bin/env python3
"""
Activity Data Validator
Validates extracted activity data against project requirements
"""

import re
from datetime import datetime
from typing import Dict, List, Tuple
import yaml
from pathlib import Path


class ActivityValidator:
    """Validates activity data structure and content"""

    # Supported time zones
    VALID_TIMEZONES = {
        "Asia/Shanghai", "Asia/Tokyo", "Asia/Hong_Kong", "Asia/Bangkok",
        "America/New_York", "America/Los_Angeles", "America/Chicago",
        "Europe/London", "Europe/Paris", "Europe/Berlin",
        "UTC", "Etc/UTC"
    }
    
    # Valid categories
    VALID_CATEGORIES = {"activity", "conference", "competition"}

    def __init__(self):
        self.data_dir = Path("data")
        self.errors = []
        self.warnings = []

    def validate_id_uniqueness(self, event_id: str, category: str) -> bool:
        """Check if event ID is unique across all categories"""
        for cat_file in self.data_dir.glob("*.yml"):
            try:
                with open(cat_file, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f) or []
                    for item in data:
                        if isinstance(item, dict) and 'events' in item:
                            for event in item['events']:
                                if isinstance(event, dict) and event.get('id') == event_id:
                                    self.errors.append(
                                        f"Event ID '{event_id}' 已存在于 {cat_file.name}"
                                    )
                                    return False
            except Exception as e:
                self.warnings.append(f"检查 {cat_file.name} 时出错: {e}")
        return True

    def validate_iso8601_datetime(self, datetime_str: str) -> bool:
        """Validate ISO 8601 datetime format"""
        pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}$'
        if not re.match(pattern, datetime_str):
            self.errors.append(
                f"无效的ISO 8601时间格式: {datetime_str}，应为 YYYY-MM-DDTHH:mm:ss"
            )
            return False
        
        try:
            datetime.fromisoformat(datetime_str)
            return True
        except ValueError as e:
            self.errors.append(f"无效的日期: {datetime_str} - {e}")
            return False

    def validate_timezone(self, timezone: str) -> bool:
        """Validate timezone is IANA standard"""
        if timezone not in self.VALID_TIMEZONES:
            self.warnings.append(
                f"非标准时区: {timezone}，建议使用标准IANA时区"
            )
            # Don't fail on this, just warn
            return True
        return True

    def validate_activity_data(self, data: Dict) -> Tuple[bool, List[str], List[str]]:
        """
        Validate complete activity data structure
        Returns (is_valid, errors, warnings)
        """
        self.errors = []
        self.warnings = []
        
        # Required fields
        required_fields = {
            "title": str,
            "description": str,
            "category": str,
            "tags": list,
            "events": list
        }
        
        for field, field_type in required_fields.items():
            if field not in data:
                self.errors.append(f"缺少必需字段: {field}")
                continue
            
            if not isinstance(data[field], field_type):
                self.errors.append(
                    f"字段 {field} 类型错误: 期望 {field_type.__name__}，"
                    f"得到 {type(data[field]).__name__}"
                )
        
        # Validate category
        if data.get("category") not in self.VALID_CATEGORIES:
            self.errors.append(
                f"无效的category: {data.get('category')}，"
                f"应为: {', '.join(self.VALID_CATEGORIES)}"
            )
        
        # Validate description length
        if len(data.get("description", "")) > 100:
            self.warnings.append(
                f"描述过长: {len(data.get('description'))}字，建议不超过100字"
            )
        
        # Validate title length
        if len(data.get("title", "")) > 50:
            self.warnings.append(
                f"标题过长: {len(data.get('title'))}字，建议不超过50字"
            )
        
        # Validate tags
        tags = data.get("tags", [])
        if len(tags) > 5:
            self.warnings.append(f"标签过多: {len(tags)}个，建议不超过5个")
        
        if len(tags) == 0:
            self.warnings.append("没有添加任何标签")
        
        # Validate events
        events = data.get("events", [])
        if not events:
            self.errors.append("必须至少有一个event")
        
        for i, event in enumerate(events):
            self._validate_event(event, i, data.get("category", "activity"))
        
        return len(self.errors) == 0, self.errors, self.warnings

    def _validate_event(self, event: Dict, event_index: int, category: str):
        """Validate individual event structure"""
        prefix = f"Event #{event_index}: "
        
        # Required event fields
        required_event_fields = {
            "year": (int, "年份"),
            "id": (str, "事件ID"),
            "link": (str, "链接"),
            "timeline": (list, "时间线"),
            "timezone": (str, "时区"),
            "date": (str, "日期"),
            "place": (str, "地点")
        }
        
        for field, (field_type, field_name) in required_event_fields.items():
            if field not in event:
                self.errors.append(f"{prefix}缺少必需字段: {field_name} ({field})")
                continue
            
            if not isinstance(event[field], field_type):
                self.errors.append(
                    f"{prefix}{field_name}类型错误: 期望{field_type.__name__}，"
                    f"得到{type(event[field]).__name__}"
                )
        
        # Validate year range
        year = event.get("year")
        if isinstance(year, int):
            if year < 2020 or year > 2030:
                self.warnings.append(f"{prefix}年份 {year} 超出合理范围 (2020-2030)")
        
        # Validate ID uniqueness
        if isinstance(event.get("id"), str):
            self.validate_id_uniqueness(event.get("id"), category)
        
        # Validate link format
        link = event.get("link", "")
        if link and not (link.startswith("http://") or link.startswith("https://")):
            self.errors.append(f"{prefix}链接格式不正确: {link}")
        
        # Validate timezone
        if isinstance(event.get("timezone"), str):
            self.validate_timezone(event.get("timezone"))
        
        # Validate timeline
        timeline = event.get("timeline", [])
        if not isinstance(timeline, list) or not timeline:
            self.errors.append(f"{prefix}时间线不能为空")
        else:
            for j, deadline in enumerate(timeline):
                if not isinstance(deadline, dict):
                    self.errors.append(f"{prefix}Timeline #{j} 必须是对象")
                    continue
                
                if "deadline" not in deadline:
                    self.errors.append(f"{prefix}Timeline #{j} 缺少deadline字段")
                elif isinstance(deadline.get("deadline"), str):
                    self.validate_iso8601_datetime(deadline.get("deadline"))
                
                if "comment" not in deadline:
                    self.warnings.append(f"{prefix}Timeline #{j} 缺少comment字段")
        
        # Validate date format (should be human-readable)
        date_str = event.get("date", "")
        if date_str and not re.search(r'\d{4}年\d{1,2}月\d{1,2}日', date_str):
            self.warnings.append(
                f"{prefix}日期格式建议使用中文，如: '2025年4月30日' 或 '2025年4月30日-9月30日'"
            )


def validate_yaml_file(file_path: Path) -> Tuple[bool, str]:
    """
    Validate YAML file structure
    Returns (is_valid, message)
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        if not isinstance(data, list):
            return False, "YAML文件顶级必须是列表"
        
        validator = ActivityValidator()
        all_valid = True
        all_errors = []
        all_warnings = []
        
        for i, item in enumerate(data):
            if not isinstance(item, dict):
                all_errors.append(f"Item #{i} 必须是对象")
                all_valid = False
                continue
            
            is_valid, errors, warnings = validator.validate_activity_data(item)
            all_valid = all_valid and is_valid
            all_errors.extend([f"Item #{i}: {e}" for e in errors])
            all_warnings.extend([f"Item #{i}: {w}" for w in warnings])
        
        message = ""
        if all_errors:
            message += "❌ 错误:\n" + "\n".join(f"  - {e}" for e in all_errors) + "\n"
        if all_warnings:
            message += "⚠️ 警告:\n" + "\n".join(f"  - {w}" for w in all_warnings) + "\n"
        
        if not message:
            message = "✅ 验证通过"
        
        return all_valid, message
    
    except Exception as e:
        return False, f"无法解析YAML文件: {str(e)}"


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("使用方法: python validate_activity.py <yaml_file_path>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    is_valid, message = validate_yaml_file(file_path)
    
    print(message)
    sys.exit(0 if is_valid else 1)
