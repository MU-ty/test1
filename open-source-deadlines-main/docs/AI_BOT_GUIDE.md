# AI Activity Bot 使用指南

## 概述

AI Activity Bot 是一个GitHub Action工作流，可以自动从提供的活动网址中提取并整理活动信息，大幅降低贡献成本。

## 工作流程

```
用户提交Issue
    ↓
在评论中触发Bot (@activity-bot extract <URL>)
    ↓
Bot爬取网页内容
    ↓
Claude Vision AI分析信息
    ↓
生成YAML格式数据
    ↓
在Issue中展示提取结果
    ↓
用户确认无误后触发自动PR (@activity-bot confirm)
    ↓
Maintainer审核并合并
```

## 使用方法

### 方式一：基础使用（推荐）

1. **创建新Issue**
   - 标题：`[AI Bot] 添加活动：活动名称`
   - 描述：可简要说明活动信息或者直接提供链接

2. **在Issue评论中触发Bot**
   
   使用以下命令格式触发提取：
   
   ```
   @activity-bot extract https://example.com/activity-page
   ```
   
   **参数说明：**
   - URL：必需，活动的官方网址
   - 类型指定（可选）：在命令末尾添加
     - `conference` - 表示这是一个会议
     - `competition` - 表示这是一个竞赛
     - 默认为 `activity` - 通用活动

3. **完整示例**

   **提取一个会议信息：**
   ```
   @activity-bot extract https://www.osconf.org/2025 conference
   ```

   **提取一个竞赛信息：**
   ```
   @activity-bot extract https://summer-ospp.ac.cn competition
   ```

   **提取一个通用活动：**
   ```
   @activity-bot extract https://opensource-event.com
   ```

4. **查看提取结果**

   Bot会在Issue中回复一条包含以下信息的评论：
   
   - ✅ 提取的YAML格式数据
   - ✅ ID唯一性验证结果
   - ✅ 标签复用情况
   - ✅ 建议的后续步骤

5. **确认并创建PR**

   当你对提取的数据满意时，在原评论下回复：
   ```
   @activity-bot confirm
   ```
   
   Bot将自动创建Pull Request，Maintainer可以审核后合并。

### 方式二：手动调整

如果对AI提取的数据不完全满意，你可以：

1. 在Issue评论中指出需要调整的字段
2. 提供修正信息
3. Bot会尝试根据新信息重新提取或手动修改

## 数据格式说明

提取后生成的YAML格式如下：

```yaml
- title: 活动名称
  description: 对活动的一句话描述（不超过100字）
  category: activity  # 或 conference、competition
  tags:
    - 标签1
    - 标签2
  events:
    - year: 2025
      id: unique-event-id  # 全局唯一ID
      link: https://example.com
      timeline:
        - deadline: '2025-01-15T18:00:00'
          comment: '报名截止'
        - deadline: '2025-02-28T24:00:00'
          comment: '活动结束'
      timezone: Asia/Shanghai
      date: 2025年1月15日 - 2月28日
      place: 线上
```

**字段说明：**

| 字段 | 类型 | 说明 |
|-----|------|------|
| title | string | 活动名称，不超过50字 |
| description | string | 活动简介，不超过100字 |
| category | string | 类别，必须为 `activity`、`conference` 或 `competition` |
| tags | array | 标签数组，不超过5个。优先复用现有标签 |
| year | number | 活动年份 |
| id | string | 全局唯一的活动ID，格式：`name-year[-num]` |
| link | string | 活动官方链接 |
| timezone | string | 时区，使用IANA标准（默认Asia/Shanghai） |
| deadline | string | ISO 8601格式时间：`YYYY-MM-DDTHH:mm:ss` |
| comment | string | 截止日期说明 |
| date | string | 人类可读格式：`2025年1月1日` 或 `2025年1月1日-2月28日` |
| place | string | 地点，如 `线上` 或 `国家，城市` |

## Bot工作原理

### 1. 网页内容提取
- 访问提供的URL
- 提取网页HTML中的文本内容
- 清理脚本、样式等无关内容

### 2. AI分析
- 使用GitHub Models API中的Claude 3.5 Sonnet模型
- 分析文本内容识别活动关键信息
- 生成结构化JSON数据

### 3. 数据验证
- **ID唯一性**：检查新ID是否与现有ID冲突
- **标签检查**：如存在类似标签，优先使用现有标签
- **数据完整性**：检查所有必需字段是否填充

### 4. 格式转换
- 将JSON转换为YAML格式
- 附加到对应类别文件（activities.yml/conferences.yml/competitions.yml）
- 创建Pull Request供Maintainer审核

## 常见问题

### Q: Bot无法访问某个网址怎么办？

**A:** 可能原因：
- 网址不可达或服务器拒绝访问
- 页面需要登录或JavaScript渲染
- 网址指向的是链接而非活动详情页

**解决方案：**
1. 确保URL直接指向活动详情页面
2. 尝试提供备用URL（如活动的规则说明页面）
3. 在Issue中直接粘贴活动详情文本，让Bot分析

### Q: AI提取的信息不准确怎么办？

**A:** 虽然Bot会进行最大努力分析，但复杂的页面布局可能导致信息混乱。此时：

1. 在Issue中指出错误信息
2. 提供正确的信息
3. 询问Bot重新提取或手动修改

或者直接按照标准格式手动提交修改PR。

### Q: 标签能否创建新的？

**A:** 可以。Bot会优先复用现有标签以保持一致性，但当需要新标签时也会创建。新标签需要：
- 简洁明确（2-5字为宜）
- 与现有标签风格一致
- 在Maintainer审核时也会检查

### Q: 如何确保时间格式正确？

**A:** 
- **Deadline** 必须是ISO 8601格式：`2025-01-15T18:00:00`
- **Date** 使用中文格式：`2025年1月15日` 或范围 `2025年1月15日-2月28日`
- **Timezone** 使用标准IANA时区，如 `Asia/Shanghai`、`America/New_York`

Bot会自动验证这些格式。

### Q: 可以批量添加多个活动吗？

**A:** 目前建议为每个活动单独创建Issue和触发Bot。如果有批量需求，可以：
1. 创建单个Issue
2. 多次触发Bot（每条评论一个活动）
3. 全部验证后统一创建PR

## 集成建议

### 1. 在README中添加指引

在项目README的"如何添加活动"部分，添加：

```markdown
### 自动化方式（推荐新贡献者使用）

如果不熟悉YAML格式，可以使用我们的AI Bot自动提取：

1. 创建Issue，标题为 `[AI Bot] 添加活动：活动名称`
2. 在评论中使用：`@activity-bot extract <活动URL>`
3. Bot会自动分析网页并生成格式化数据
4. 确认无误后回复：`@activity-bot confirm`
5. Bot会自动创建PR供审核

详见 [AI Bot 使用指南](docs/AI_BOT_GUIDE.md)
```

### 2. Issue模板

创建 `.github/ISSUE_TEMPLATE/add-activity-ai.md`：

```markdown
---
name: 使用AI Bot添加活动
about: 通过AI Bot快速添加开源活动信息
title: '[AI Bot] 添加活动：'
labels: 'ai-bot,待处理'
---

## 活动链接
<!-- 粘贴活动的官方网址 -->


## 活动类型
- [ ] 活动（activity）
- [ ] 会议（conference）
- [ ] 竞赛（competition）

## 说明
<!-- 可选：对活动的额外说明 -->


## 如何继续
1. 请在下方评论中使用以下命令：
```
@activity-bot extract <your-activity-url> <category>
```

例如：
```
@activity-bot extract https://example.com/activity activity
```

2. 等待Bot分析并给出结果
3. 确认无误后，回复：`@activity-bot confirm`
4. Bot将自动创建Pull Request
```

### 3. 标签管理

在GitHub中创建标签：
- `ai-bot` - AI Bot相关的Issues
- `auto-extract` - 由Bot自动提取的数据
- `待审核` - 等待Maintainer审核的PR

## 技术细节

### GitHub Models API

Bot使用GitHub Models API中的Claude 3.5 Sonnet：

```python
endpoint = "https://models.inference.ai.azure.com/chat/completions"
model = "claude-3-5-sonnet"
```

**免费额度信息：** GitHub提供一定额度的免费调用（详见官方文档）

### 环境变量配置

在GitHub仓库Settings中配置：
- `GITHUB_TOKEN` - 自动提供，用于API调用和PR创建

### 依赖包

```
PyYAML>=2
requests>=2
Pillow>=10  # 未来用于OCR
pydantic>=2  # 数据验证
```

## 后续改进方向

### Phase 1（当前）
- ✅ 网页文本提取
- ✅ AI分析与结构化
- ✅ YAML生成
- ✅ ID/标签验证

### Phase 2（计划）
- 📋 支持上传图片/PDF
- 📋 OCR提取文字
- 📋 QR码识别
- 📋 自动网址规范化（找到官网链接）

### Phase 3（计划）
- 📋 与Google Events API集成
- 📋 自动更新活动状态
- 📋 重复活动检测
- 📋 多语言支持

## 反馈与贡献

如有问题或改进建议，请：
1. 在Discussions中讨论
2. 提交Issue报告bug
3. 直接提交改进PR

---

**最后更新**：2025年1月
**维护者**：@your-username
