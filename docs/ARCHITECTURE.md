# AI Activity Bot - 完整系统说明

## 📐 系统架构

```
┌─────────────────────────────────────────────────────────────────┐
│                    用户在GitHub Issue中                          │
│            发起命令：@activity-bot extract <URL>               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
        ┌───────────────────────────────────────┐
        │  GitHub Actions Workflow Trigger      │
        │  (activity-extractor-bot.yml)         │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  1. 解析Issue评论获取URL和参数        │
        │     - URL提取                         │
        │     - 活动类型识别                    │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  2. 网页内容爬取                       │
        │     - HTTP请求获取HTML                │
        │     - 清理脚本和样式标签              │
        │     - 提取文本内容                    │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  3. AI分析和提取 (extract_activity.py)│
        │     - 调用GitHub Models API           │
        │     - Claude 3.5 Sonnet分析           │
        │     - 结构化信息提取                  │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  4. 数据验证 (validate_activity.py)   │
        │     - ID唯一性检查                    │
        │     - 标签规范化                      │
        │     - 字段完整性校验                  │
        │     - 日期格式验证                    │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  5. YAML生成和格式转换                │
        │     - JSON转YAML                      │
        │     - 保存至ai-bot-results.json      │
        └───────────────┬─────────────────────┘
                        │
                        ▼
        ┌───────────────────────────────────────┐
        │  6. 结果回复                          │
        │     - 在Issue评论中展示结果           │
        │     - 验证信息反馈                    │
        │     - 后续操作提示                    │
        └───────────────┬─────────────────────┘
                        │
        ┌───────────────┴─────────────────────┐
        │                                      │
        ▼                                      ▼
用户确认无误            用户需要调整或失败
    │                          │
    │                          └─► 在Issue中说明
    │                              并请求重试
    ▼
@activity-bot confirm
    │
    ▼
创建Pull Request
    │
    ▼
Maintainer审核和合并
```

## 📁 文件结构

```
open-source-deadlines/
├── .github/
│   ├── workflows/
│   │   └── activity-extractor-bot.yml       ⭐ 主工作流文件
│   └── ISSUE_TEMPLATES/
│       ├── add-activity-ai-bot.md           📝 AI Bot使用模板
│       └── add-activity-manual.md           📝 手动添加模板
├── scripts/
│   └── ai-bot/
│       ├── extract_activity.py              🤖 核心提取脚本
│       ├── validate_activity.py             ✅ 数据验证脚本
│       └── requirements.txt                 📦 Python依赖
├── docs/
│   ├── AI_BOT_GUIDE.md                      📖 用户使用指南
│   └── DEPLOYMENT_GUIDE.md                  🚀 部署配置指南
├── data/
│   ├── activities.yml                       📊 活动数据
│   ├── conferences.yml                      📊 会议数据
│   └── competitions.yml                     📊 竞赛数据
└── README.md                                📖 项目说明
```

## 🔄 数据流向

### 输入
```
用户提供：活动URL
  ↓
系统提取：网页文本内容 + 元信息
  ↓
AI分析：识别活动名称、日期、地点等
```

### 处理
```
JSON结构化数据
  ↓
验证ID唯一性
  ↓
规范化标签和时区
  ↓
检查字段完整性
```

### 输出
```
YAML格式化输出
  ↓
Issue评论展示
  ↓
自动创建PR（用户确认后）
  ↓
Maintainer合并
```

## 🎯 核心功能模块

### 1. ActivityExtractor类
**文件：** `scripts/ai-bot/extract_activity.py`

**主要方法：**

| 方法 | 功能 |
|------|------|
| `_fetch_webpage_content()` | 获取网页HTML内容 |
| `_extract_text_from_html()` | 从HTML中提取纯文本 |
| `_call_claude_vision_api()` | 调用AI模型进行分析 |
| `_parse_claude_response()` | 解析AI返回的JSON |
| `_generate_event_id()` | 生成唯一的事件ID |
| `_normalize_tags()` | 规范化和去重标签 |
| `extract()` | 主流程编排 |

**关键特性：**
- ✅ 自动去重标签（优先复用现有标签）
- ✅ ID冲突检测和自动递增处理
- ✅ 灵活的网页解析
- ✅ 结构化数据输出

### 2. ActivityValidator类
**文件：** `scripts/ai-bot/validate_activity.py`

**验证项：**

| 项目 | 检查内容 |
|------|---------|
| ID唯一性 | 确保ID在所有YAML文件中唯一 |
| 日期格式 | ISO 8601格式验证 |
| 时区标准 | IANA标准时区验证 |
| 字段完整 | 所有必需字段存在 |
| 字段类型 | 字段类型匹配 |
| 长度限制 | title<50字，description<100字 |
| 标签数量 | 最多5个标签 |
| 链接格式 | URL格式正确性 |

### 3. GitHub Actions工作流
**文件：** `.github/workflows/activity-extractor-bot.yml`

**两个主要Job：**

#### Job 1: extract-activity
触发：`@activity-bot extract <URL>`

```yaml
步骤：
1. 检出代码
2. 设置Python环境
3. 安装依赖
4. 解析Issue评论
5. 执行extract_activity.py
6. 在Issue中回复结果
```

#### Job 2: create-pull-request
触发：`@activity-bot confirm`

```yaml
步骤：
1. 检出代码
2. 读取ai-bot-results.json
3. 使用create-pull-request action
4. 自动提交PR
5. 设置自动删除分支
```

## 🧬 AI提示词设计

### 提示词结构

```python
extraction_prompt = """
请从以下网页内容中提取开源活动的结构化信息

[包含以下核心元素：]
1. 提取什么（字段列表）
2. 格式要求（JSON结构）
3. 重点提示（重要字段和格式）
4. 容错处理（如何处理缺失字段）
"""
```

### 优化策略

1. **清晰的字段定义**
   ```
   - title: 活动名称（不超过50字）
   - description: 一句话描述（不超过100字）
   ```

2. **明确的格式要求**
   ```
   - ISO 8601: YYYY-MM-DDTHH:mm:ss
   - 时区：使用IANA标准
   ```

3. **示例指导**
   ```
   返回格式:
   ```json
   {...}
   ```
   ```

4. **容错处理**
   ```
   如果无法确定，使用null
   不要猜测，只提取明确的信息
   ```

## 🔐 安全和隐私

### 输入安全
- ✅ URL验证（必须是http/https）
- ✅ 超时控制（10秒）
- ✅ 异常处理

### 数据处理
- ✅ 仅处理公开网页内容
- ✅ 不存储用户个人信息
- ✅ 清理HTML脚本标签

### 输出安全
- ✅ 人工审核机制
- ✅ Maintainer最终把关
- ✅ PR review流程

## 🚀 性能优化

### 当前性能指标

| 指标 | 值 |
|------|-----|
| 平均提取时间 | 30-60秒 |
| API调用延迟 | 5-10秒 |
| 网页爬取时间 | 2-5秒 |
| 数据验证时间 | <1秒 |

### 优化方向

1. **缓存策略**
   - 缓存常见URL的分析结果
   - 预加载现有标签和ID列表

2. **并行处理**
   - 同时处理多个Issues的请求
   - （当前GitHub Actions已支持）

3. **模型选择**
   - 根据内容复杂度选择合适模型
   - Haiku用于简单页面，Sonnet用于复杂页面

## 📈 扩展方向

### Phase 2：图片和OCR支持
```python
# 未来计划
from PIL import Image
import pytesseract

# 处理上传的活动海报或截图
def extract_text_from_image(image_path):
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image, lang='chi_sim')
    return text
```

### Phase 3：高级功能
- 🔍 QR码识别和链接提取
- 🌐 自动网址规范化（寻找官网链接）
- 📅 与Google Calendar API集成
- 🔄 自动更新已过期的活动状态
- 🌍 多语言支持

### Phase 4：智能决策
- 🤖 学习Maintainer的审核反馈
- 🎯 自动检测和合并重复活动
- 💡 推荐类似的活动标签
- ⚡ 优化AI模型选择

## 📊 监控指标

### 可跟踪的指标

```python
{
  "total_extractions": 150,           # 总提取次数
  "successful_rate": 0.92,            # 成功率
  "avg_extraction_time": 45,          # 平均提取时间(秒)
  "tags_created": 23,                 # 新建标签数
  "tags_reused": 127,                 # 复用标签数
  "api_errors": 12,                   # API错误次数
  "validation_failures": 8,           # 验证失败次数
}
```

### 分析仪表板（计划）

```
Monthly Statistics
├── 提取成功率
├── 平均处理时间
├── API使用量
├── 新建vs复用标签比
└── 常见错误类型
```

## 🤝 社区集成

### 在README中推荐
```markdown
### 自动化方式（推荐新贡献者）

使用我们的AI Bot，只需提供活动链接：

```
@activity-bot extract https://example.com
```

详见 [AI Bot使用指南](docs/AI_BOT_GUIDE.md)
```

### 贡献者体验流程
```
零基础贡献者
    ↓
找到活动链接
    ↓
创建Issue（用模板）
    ↓
触发Bot命令
    ↓
1-2分钟获得结果
    ↓
验证无误后确认
    ↓
自动PR创建
    ↓
Maintainer合并
    ↓
✅ 贡献完成！
```

## 📚 知识库

### 相关技术
- [GitHub Actions API](https://docs.github.com/en/actions)
- [Claude API](https://docs.anthropic.com/)
- [YAML规范](https://yaml.org/)
- [ISO 8601标准](https://en.wikipedia.org/wiki/ISO_8601)

### 最佳实践
- 使用强类型验证
- 优先级：自动化 > 手动干预
- 透明的错误提示
- 详细的审核日志

---

## 🎓 学习资源

项目中所有脚本都包含：
- ✅ 详细的注释说明
- ✅ Type hints类型提示
- ✅ 错误处理示例
- ✅ 文档字符串

适合学习以下内容：
- GitHub Actions工作流编程
- AI API集成实践
- Python数据处理
- 开源项目自动化
- CLI工具设计

---

**系统设计目标**

✨ **降低贡献门槛** - 从零基础到成功贡献 <5分钟  
⚡ **提高效率** - 自动化繁琐的整理流程  
🤖 **AI赋能** - 让机器完成重复劳动  
✅ **保证质量** - 多层验证确保数据准确  
🌟 **优化体验** - 清晰的反馈和引导  

---

**最后更新**：2025年1月  
**维护者**：[@your-github-username]
