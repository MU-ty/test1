# AI Bot 完整使用指南

## 📖 目录

1. [快速开始](#快速开始)
2. [命令参考](#命令参考)
3. [工作流程](#工作流程)
4. [实际示例](#实际示例)
5. [常见问题](#常见问题)
6. [高级用法](#高级用法)

## 🚀 快速开始

### 前提条件

1. ✅ 已配置 `GH_MODELS_TOKEN` secret
2. ✅ 仓库中有 `.github/workflows/ai-bot-handler.yml` 文件
3. ✅ `scripts/ai-bot/` 目录包含所有必需的 Python 模块

### 最快上手（3步）

**第1步**: 创建新 Issue  
**第2步**: 输入命令
```
@activity-bot extract https://example.com/event activity
```
**第3步**: 等待结果，然后确认
```
@activity-bot confirm
```

## 📋 命令参考

### 基本命令

#### 1. `extract` - 提取活动信息

**格式**:
```
@activity-bot extract <URL> [category]
```

**参数**:
| 参数 | 类型 | 必需 | 说明 |
|------|------|------|------|
| URL | 字符串 | ✅ | 要爬取的网页链接 |
| category | 字符串 | ❌ | 活动类型，默认为 `activity` |

**支持的分类**:
- `activity` - 一般活动、讲座、工作坊
- `conference` - 技术会议
- `competition` - 编程竞赛

**示例**:
```bash
# 最简单的用法
@activity-bot extract https://github.com/python/cpython/discussions

# 指定活动类型为会议
@activity-bot extract https://www.pycon.org 2024 conference

# 竞赛活动
@activity-bot extract https://codeforces.com/contests competition
```

**预期输出**:
- 处理中消息（1-2分钟内）
- 提取结果包含：
  - 活动标题
  - 活动描述
  - 日期信息
  - 位置
  - 标签
  - 来源链接

#### 2. `confirm` - 确认提取结果

**格式**:
```
@activity-bot confirm
```

**功能**:
- 确认上一次的提取结果
- 触发自动创建 Pull Request
- PR 将包含更新到相应 YAML 文件的更改

**注意**:
- 必须在上一次 extract 成功后使用
- 会自动创建 PR，检查内容后再合并

**示例工作流**:
```
Issue #123:
  1. User: @activity-bot extract https://example.com activity
  2. Bot: 处理中... [1分钟后]
  3. Bot: 提取结果如下...
  4. User: @activity-bot confirm
  5. Bot: 已创建 PR #456
  6. Maintainer: 审查 PR #456
  7. Maintainer: 合并 PR
```

## 🔄 工作流程

### 完整流程图

```
┌─────────────────────────────────────────────────────┐
│ 用户在 Issue 中输入命令                              │
│ @activity-bot extract <URL> <category>              │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ GitHub Actions 检测到 issue_comment 事件            │
│ ├─ 解析命令和参数                                   │
│ ├─ 验证 URL 有效性                                  │
│ └─ 启动 bot_handler.py                              │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ Step 1: 网页爬取 (WebScraper)                       │
│ ├─ 获取 HTML 内容                                   │
│ ├─ 提取文本                                         │
│ └─ 提取元数据 (标题、描述等)                        │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ Step 2: AI 分析 (ActivityAnalyzer)                  │
│ ├─ 使用 Claude/GPT-4 分析文本                       │
│ ├─ 提取结构化数据                                   │
│ │  ├─ title (标题)                                  │
│ │  ├─ description (描述)                            │
│ │  ├─ start_date / end_date (日期)                  │
│ │  ├─ location (位置)                               │
│ │  └─ tags (标签)                                   │
│ └─ 返回 JSON 格式结果                               │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ Step 3: 数据验证 (DataValidator)                    │
│ ├─ 检查必需字段                                     │
│ ├─ 验证日期格式                                     │
│ ├─ 检查 ID 唯一性                                   │
│ ├─ 标准化标签                                       │
│ └─ 返回验证结果                                     │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ Step 4: YAML 生成                                   │
│ ├─ 生成活动 ID                                      │
│ ├─ 格式化数据为 YAML                                │
│ └─ 保存为 JSON 艺术品                               │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ 在 Issue 中回复提取结果                              │
│ ✓ 成功：显示提取的数据                              │
│ ✗ 失败：显示错误信息                                │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ 用户审查结果                                        │
│ 如果满意，输入：@activity-bot confirm               │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ 第二个 GitHub Actions 任务触发                      │
│ ├─ 加载之前保存的结果                               │
│ ├─ 创建 Git 分支                                    │
│ ├─ 更新相应的 YAML 文件                             │
│ │  └─ data/activity.yml                             │
│ │  └─ data/conference.yml                           │
│ │  └─ data/competition.yml                          │
│ ├─ 提交变更                                         │
│ └─ 创建 Pull Request                                │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ Maintainer 审查 PR                                  │
│ ├─ 检查提取的数据                                   │
│ ├─ 必要时进行手动编辑                               │
│ └─ 合并 PR                                          │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ ✅ 完成！活动数据已添加到仓库                        │
└─────────────────────────────────────────────────────┘
```

## 💡 实际示例

### 示例 1: 添加 Python 会议

**场景**: 你想添加 PyCon 2024 会议到仓库

**步骤1**: 创建 Issue
```
标题: Add PyCon 2024 to conferences
内容: 请帮助添加 PyCon 2024 会议信息
```

**步骤2**: 在 Issue 中回复
```
@activity-bot extract https://us.pycon.org/2024 conference
```

**Bot 响应** (1-2分钟后):
```
✓ 提取成功！

标题: PyCon US 2024
描述: The premier Python conference in the US...
开始日期: 2024-05-15
结束日期: 2024-05-23
地点: Pittsburgh, Pennsylvania
标签: [python, conference, tech]
来源: https://us.pycon.org/2024
```

**步骤3**: 确认结果
```
看起来不错，谢谢！
@activity-bot confirm
```

**Bot 创建 PR**
```
✓ 已创建 PR #123
类型: 添加会议
更新文件: data/conferences.yml
预览:
  - title: PyCon US 2024
    tags: [python, conference, tech]
    events:
      - year: 2024
        id: pyccon-us-202405
        date: 2024-05-15~2024-05-23
        place: Pittsburgh, Pennsylvania
        link: https://us.pycon.org/2024
```

### 示例 2: 添加 CTF 竞赛

**命令**:
```
@activity-bot extract https://ctftime.org/event/1234 competition
```

### 示例 3: 添加开源工作坊

**命令**:
```
@activity-bot extract https://github.com/example/workshop activity
```

## ❓ 常见问题

### Q1: 提取失败，提示 "缺少GH_MODELS_TOKEN"
**答**: 你需要在仓库 Settings → Secrets 中配置 `GH_MODELS_TOKEN`。参见快速启动指南。

### Q2: 提取需要多久？
**答**: 通常 1-2 分钟。如果超过 5 分钟，请检查 GitHub Actions 日志。

### Q3: 提取的信息不完整怎么办？
**答**: 这很正常。AI 模型有时无法从所有网页中提取完整信息。你可以：
1. 在 confirm 前手动编辑提取的信息
2. 或者使用传统方式手动提交

### Q4: 可以提取中文网站的内容吗？
**答**: 可以，系统支持任何语言的网页。

### Q5: 如何修改已经创建的 PR？
**答**: 可以直接编辑 PR 中的文件，或关闭 PR 后重新提交。

### Q6: 一个 Issue 中可以提取多次吗？
**答**: 可以，但每次 extract 都会覆盖之前的结果。建议为每个活动创建单独的 Issue。

### Q7: 支持哪些网站？
**答**: 支持大多数公开网站。某些需要登录或有特殊防护的网站可能无法爬取。

### Q8: 如何获取更多示例或帮助？
**答**: 查看本仓库的：
- Issues - 查看已解决的问题
- Discussions - 社区讨论
- Documentation - 详细文档

## 🎯 高级用法

### 批量提交多个活动

如果需要一次性添加多个活动，可以创建多个 Issue 或在同一个 Issue 中提交多条命令：

```
@activity-bot extract https://example.com/event1 activity
@activity-bot extract https://example.com/event2 conference
@activity-bot extract https://example.com/event3 competition
```

Bot 会按顺序处理每个命令。

### 自定义数据字段

如需添加标准字段之外的信息，可以在 confirm 前手动编辑提取的数据。

### 与 CI/CD 集成

Bot 生成的 PR 会自动触发项目的 CI/CD 流程，包括：
- 数据格式验证
- 自动化测试
- 部署预览

## 📊 支持的活动信息

### 自动提取的字段

- ✅ `title` - 活动标题
- ✅ `description` - 活动描述
- ✅ `start_date` - 开始日期
- ✅ `end_date` - 结束日期
- ✅ `location` - 活动地点
- ✅ `tags` - 标签
- ✅ `url` - 源网址
- ✅ `registration_url` - 报名链接（如果存在）

### 数据格式

所有字段都遵循特定格式：

```yaml
- id: event-id-202405
  title: Event Title
  description: Event description here
  tags: [tag1, tag2, tag3]
  events:
    - year: 2024
      id: event-id-202405
      date: 2024-05-15~2024-05-23
      time: "09:00-17:00"
      place: Location or "Online"
      timezone: Asia/Shanghai
      link: https://example.com
```

## 🔗 相关资源

- 📚 [快速启动指南](./QUICKSTART.md)
- 📋 [部署检查清单](./DEPLOYMENT_CHECKLIST.md)
- 🔌 [API 集成指南](./AI_BOT_API_GUIDE.md)
- 🐛 [故障排查](./TROUBLESHOOTING.md)

---

**最后更新**: 2024年  
**版本**: 1.0  
**维护者**: AI Bot Team  
**许可证**: MIT
