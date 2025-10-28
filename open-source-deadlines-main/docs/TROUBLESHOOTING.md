# 🔧 AI Bot 快速故障排查指南

## 🚨 常见问题速查表

### Bot无响应

**症状**：提交命令后，Bot没有在5分钟内回复

| 原因 | 检查方法 | 解决方案 |
|-----|--------|--------|
| 命令格式错误 | 检查@活动机器人和URL | 使用正确格式：`@activity-bot extract https://example.com` |
| GitHub Actions未启用 | Settings → Actions → General | 启用"Allow all actions and reusable workflows" |
| 工作流文件有问题 | Actions标签查看失败日志 | 检查YAML语法或重新上传文件 |
| 网络问题 | 尝试其他Issue | 等待几分钟重试 |

**快速排查清单：**
```
☐ 命令中有 @activity-bot extract
☐ URL以 https:// 开头
☐ 没有多余空格
☐ GitHub Actions已启用
☐ .github/workflows/activity-extractor-bot.yml 存在
```

---

### 提取失败

**症状**：Bot回复"❌ 提取失败"

**常见原因和解决：**

#### 1️⃣ URL无法访问
```
错误信息：无法访问提供的URL

原因：
- 网址输入错误
- 网站不可达
- Bot被服务器阻止

解决：
1. 复制粘贴URL以避免手输错误
2. 在浏览器中测试链接是否有效
3. 尝试提供网站的其他页面（如规则说明页）
4. 如网站有防护，提供活动信息文本
```

#### 2️⃣ 网页内容过少
```
错误信息：网页内容过少，无法提取有效信息

原因：
- URL指向的页面信息不足
- 内容主要由JavaScript渲染（Bot无法执行JS）

解决：
1. 确保URL指向包含完整信息的页面
2. 寻找静态内容页面（不是js渲染的）
3. 在Issue中直接粘贴活动信息文本
```

#### 3️⃣ AI分析失败
```
错误信息：AI分析失败或无法解析响应

原因：
- GitHub Models API暂时不可用
- 提示词不适应此类型页面
- API超时或限流

解决：
1. 稍后重试（通常几分钟内恢复）
2. 尝试提供更清晰的URL
3. 在Issue中补充说明信息
4. 或手动提交PR
```

---

### 信息提取不准确

**症状**：Bot返回了信息，但部分字段错误

**常见错误：**

| 错误 | 原因 | 调整方法 |
|------|------|--------|
| 活动名称错误 | 网页中有多个标题 | 在Issue中指正，请求重新提取 |
| 日期错误 | 混淆了报名和活动时间 | 提供正确的日期信息 |
| 地点错误 | 识别了主办方而非活动地点 | 说明正确的地点 |
| 链接错误 | 提取了参考链接而非官方链接 | 提供官方链接 |

**修正流程：**
```
1. 在Bot的回复下发送新评论
2. 指出具体错误和正确信息
3. 请求Bot重新处理或手动修改
4. 或直接修改并@Bot确认

示例：
"地点应该是'线上'而非'北京'。
其他信息正确。
@activity-bot re-extract"
```

---

### ID冲突

**症状**：提取结果中显示"ID已存在"

**这不是问题！** Bot已自动处理：
- 检测到冲突
- 自动添加后缀（-1, -2等）
- 生成唯一ID

**你需要做的：** 
- 无需担心，继续确认即可
- Bot确保了全局唯一性 ✅

---

### 标签问题

**症状**：标签未按预期规范化

**检查项：**

```
✓ 标签是否已存在？
  → Bot会复用现有标签

✓ 创建的标签是否合理？
  → 新标签需Maintainer审核

✓ 标签数量是否超过5个？
  → Bot会警告，需要调整
```

**调整标签：**
```
1. 在Issue中建议更改
2. 指明不需要的标签
3. 建议替代标签
4. @activity-bot re-extract（重新提取）
```

---

## 🔧 本地调试

### 测试提取脚本

```bash
# 1. 设置环境变量
export GITHUB_TOKEN="your-token"
export ACTIVITY_URL="https://summer-ospp.ac.cn"
export ACTIVITY_CATEGORY="competition"
export ISSUE_NUMBER="123"

# 2. 运行脚本
cd scripts/ai-bot
python extract_activity.py

# 3. 查看结果
cat ai-bot-results.json | python -m json.tool
```

**期望输出：**
```json
{
  "success": true,
  "yaml_content": "- title: ...",
  "category": "competition",
  "validation": {
    "id_unique": true,
    "tags_info": "..."
  }
}
```

### 测试验证脚本

```bash
# 验证数据文件
python scripts/ai-bot/validate_activity.py data/activities.yml

# 期望输出：
# ✅ 验证通过

# 或者：
# ❌ 错误: ...
# ⚠️ 警告: ...
```

### 测试YAML格式

```bash
# 检查YAML文件语法
python -c "import yaml; yaml.safe_load(open('data/activities.yml'))"

# 无输出表示正确
# 有错误会显示错误信息
```

---

## 🔍 查看工作流日志

### 通过GitHub网页

1. 进入仓库 → Actions
2. 选择 "Activity Extractor Bot" 工作流
3. 点击具体的运行记录
4. 展开每个Step查看日志

### 重要的日志位置

```
1. Parse issue comment
   → URL和类型提取情况

2. Extract activity information
   → 网页爬取和AI分析过程

3. Post results as comment
   → 最终结果和错误信息
```

### 常见错误日志

```
❌ "Failed to fetch URL"
   → 网址无法访问

❌ "Empty response from API"
   → Claude API返回空结果

❌ "JSON decode error"
   → AI返回格式不正确

❌ "Event ID already exists"
   → ID冲突（Bot会自动处理）
```

---

## 🆘 无法解决时

### 当前能做的

1. **详细描述问题**
   - 使用的命令是什么
   - 完整的错误信息
   - 涉及的URL

2. **提供相关信息**
   - 期望的结果是什么
   - 已尝试的解决方法
   - 工作流日志截图

3. **获取帮助**
   - 在Issue中标记 `ai-bot`
   - 提供详细的重现步骤
   - 附加必要的文件

### 反馈模板

```markdown
## Bug报告

### 问题描述
简单说明遇到的问题

### 重现步骤
1. 创建Issue
2. 发送命令：`@activity-bot extract ...`
3. ...

### 期望结果
应该发生什么

### 实际结果
实际发生了什么

### 错误信息
```
粘贴完整的错误信息
```

### 环境信息
- 活动URL：...
- 活动类型：...
- 工作流日志：[链接]

### 截图
附加相关截图帮助理解
```

---

## 📊 诊断清单

遇到问题时，按顺序检查：

### 基础检查
- [ ] 命令格式是否正确
- [ ] URL是否有效
- [ ] GitHub Actions是否启用
- [ ] 工作流文件是否存在

### 网络检查
- [ ] 能否在浏览器中打开URL
- [ ] 网页是否包含足够的信息
- [ ] 是否需要登录
- [ ] 是否被JS渲染

### API检查
- [ ] GitHub Token是否有效
- [ ] Claude API是否可用
- [ ] 是否超过免费额度

### 数据检查
- [ ] 提取的数据格式是否正确
- [ ] ID是否冲突
- [ ] 标签是否规范
- [ ] 日期格式是否正确

### 工作流检查
- [ ] 工作流是否完整运行
- [ ] 有没有超时
- [ ] 是否有权限问题
- [ ] 日志中是否有错误

---

## 📞 获取技术支持

### 官方资源

1. **GitHub Issues** - 报告Bug或请求功能
   - 标签：`ai-bot` `bug` `help-wanted`
   - 提供尽可能多的细节

2. **Discussions** - 讨论和提问
   - 分类：Q&A, Ideas, General
   - 社区会帮忙回答

3. **文档** - 查找答案
   - [AI_BOT_GUIDE.md](AI_BOT_GUIDE.md) - 使用
   - [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - 部署
   - [ARCHITECTURE.md](ARCHITECTURE.md) - 技术

### 寻求帮助的最佳实践

✅ 提供完整信息
✅ 包含错误日志
✅ 说明已尝试的步骤
✅ 提供重现步骤
✅ 耐心等待回复

❌ 避免仅说"不工作"
❌ 不提供必要信息
❌ 期望立即回复
❌ 在多个地方重复提问

---

## 💡 常用命令速查

### 基本命令

```bash
# 提取活动（默认为activity）
@activity-bot extract https://example.com

# 提取会议
@activity-bot extract https://example.com conference

# 提取竞赛
@activity-bot extract https://example.com competition

# 确认并创建PR
@activity-bot confirm

# 重新提取（提议的语法）
@activity-bot re-extract
```

### 本地命令

```bash
# 测试提取脚本
python scripts/ai-bot/extract_activity.py

# 验证YAML文件
python scripts/ai-bot/validate_activity.py data/activities.yml

# 检查依赖
pip list | grep -E "PyYAML|requests|pydantic"
```

---

## 📈 性能指标参考

### 预期性能

| 指标 | 预期值 | 异常值 |
|------|--------|--------|
| 响应时间 | 1-2分钟 | >5分钟 |
| 提取成功率 | >95% | <80% |
| API延迟 | 5-10秒 | >30秒 |
| YAML生成 | <1秒 | >5秒 |

### 调查过慢的提取

1. 检查网络连接
2. 查看API调用时间（日志中）
3. 检查Claude API状态
4. 尝试用更简洁的URL

---

## 🎓 进阶调试

### 启用详细日志

在工作流中设置环境变量：
```yaml
env:
  RUNNER_DEBUG: true
  ACTIONS_STEP_DEBUG: true
```

### 修改超时时间

在 `extract_activity.py` 中调整：
```python
response = requests.get(url, timeout=10)  # 改为更大的值
```

### 自定义API端点

```python
self.model_api_endpoint = "your-custom-endpoint"
```

### 添加调试输出

```python
print(f"[DEBUG] URL: {self.activity_url}")
print(f"[DEBUG] HTML length: {len(html_content)}")
print(f"[DEBUG] API response: {response.json()}")
```

---

## 🚀 优化建议

### 如果提取过慢
1. 使用更快的模型（Haiku而非Sonnet）
2. 缩减网页内容大小
3. 添加缓存机制

### 如果精度不够
1. 更新提示词
2. 提供更清晰的URL
3. 手动审核后修改

### 如果失败率高
1. 检查常见失败的URL特征
2. 调整HTML清理逻辑
3. 增加容错处理

---

## 📋 问题排查决策树

```
Bot有无响应？
├─ NO → 检查工作流/Actions配置
└─ YES
    提取成功？
    ├─ NO → 检查错误日志
    │       ├─ 网址无法访问 → 验证URL
    │       ├─ 内容过少 → 提供替代页面
    │       └─ API失败 → 稍后重试
    └─ YES
        信息准确？
        ├─ NO → 在Issue中指正
        └─ YES
            确认无误？
            ├─ NO → 要求调整
            └─ YES
                发送 @activity-bot confirm
                等待PR创建
                ✅ 完成！
```

---

**祝你排查顺利！**

如问题仍未解决，请参考完整的文档或在GitHub中提问。

---

**最后更新**：2025年1月  
**维护者**：[@your-github-username]
