# 🎯 AI Bot 快速参考

## 📋 快速命令

### 为贡献者

```bash
# 提取活动信息
@activity-bot extract https://example.com

# 提取并标记为会议
@activity-bot extract https://example.com conference

# 提取并标记为竞赛
@activity-bot extract https://example.com competition

# 确认提取结果并创建PR
@activity-bot confirm
```

## ✅ 验证清单

### 提取前
- [ ] 活动URL有效且可访问
- [ ] URL指向活动详情页面（非转载或新闻）
- [ ] 确认活动类型（activity/conference/competition）

### 提取后
- [ ] Bot成功返回提取结果
- [ ] 活动名称准确
- [ ] 日期和时间正确
- [ ] 地点信息完整
- [ ] 标签合理（≤5个）
- [ ] ID无冲突

### 确认前
- [ ] 所有信息无误
- [ ] 没有个人或敏感信息
- [ ] 格式符合项目规范
- [ ] 链接有效

## 🔧 配置要点

| 配置项 | 位置 | 状态 |
|--------|------|------|
| 工作流文件 | `.github/workflows/` | ✅ 已包含 |
| 提取脚本 | `scripts/ai-bot/` | ✅ 已包含 |
| 验证脚本 | `scripts/ai-bot/` | ✅ 已包含 |
| Issue模板 | `.github/ISSUE_TEMPLATES/` | ✅ 已包含 |
| 文档 | `docs/` | ✅ 已包含 |
| GitHub Token | 自动提供 | ✅ 无需配置 |
| API密钥 | 自动使用GITHUB_TOKEN | ✅ 无需配置 |

## 📊 数据字段快速参考

```yaml
title: 活动名           # 50字以内
description: 简介       # 100字以内
category: activity      # activity/conference/competition
tags:                   # ≤5个标签
  - 标签1
  - 标签2
events:
  - year: 2025          # 年份
    id: unique-id       # 全局唯一ID
    link: https://...   # 活动链接
    timeline:
      - deadline: 2025-01-15T18:00:00  # ISO 8601
        comment: 截止说明
    timezone: Asia/Shanghai  # IANA标准
    date: 2025年1月15日      # 中文格式
    place: 线上或国家，城市
```

## 🚨 常见错误

| 错误 | 原因 | 解决 |
|-----|-----|-----|
| Bot无响应 | 命令格式错误 | 检查@活动机器人和URL |
| URL无法访问 | 网页不可达 | 检查URL或提供替代链接 |
| 信息提取错误 | AI分析失败 | 检查网页内容或手动纠正 |
| ID冲突 | ID已存在 | Bot自动处理或建议修改 |
| 日期格式错 | 格式不标准 | 使用ISO 8601: YYYY-MM-DDTHH:mm:ss |

## 📞 获取帮助

| 问题 | 位置 |
|------|------|
| 使用问题 | [AI_BOT_GUIDE.md](AI_BOT_GUIDE.md) |
| 部署问题 | [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) |
| 系统架构 | [ARCHITECTURE.md](ARCHITECTURE.md) |
| 技术细节 | 代码注释 |

## 🎓 学习路径

1. **新贡献者** → 阅读 [AI_BOT_GUIDE.md](AI_BOT_GUIDE.md)
2. **维护者** → 阅读 [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
3. **开发者** → 阅读 [ARCHITECTURE.md](ARCHITECTURE.md)
4. **深入学习** → 阅读源代码注释

---

**完整功能需要的文件：**

✅ `.github/workflows/activity-extractor-bot.yml`  
✅ `scripts/ai-bot/extract_activity.py`  
✅ `scripts/ai-bot/validate_activity.py`  
✅ `scripts/ai-bot/requirements.txt`  
✅ `.github/ISSUE_TEMPLATES/add-activity-ai-bot.md`  
✅ `docs/AI_BOT_GUIDE.md`  
✅ `docs/DEPLOYMENT_GUIDE.md`  
✅ `docs/ARCHITECTURE.md`  

所有文件已包含在项目中！🎉
