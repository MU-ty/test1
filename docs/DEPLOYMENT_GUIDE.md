# AI Bot 配置和部署指南

## 📋 目录

1. [快速开始](#快速开始)
2. [环境配置](#环境配置)
3. [GitHub Models API设置](#github-models-api设置)
4. [工作流配置](#工作流配置)
5. [测试和调试](#测试和调试)
6. [故障排除](#故障排除)

---

## 🚀 快速开始

### 前置条件

- GitHub仓库有完整的`.github/workflows`目录权限
- GitHub Actions已启用
- 项目已包含`data/activities.yml`、`data/conferences.yml`、`data/competitions.yml`

### 1分钟部署

1. **复制工作流文件**
   ```bash
   # 已包含在项目中
   .github/workflows/activity-extractor-bot.yml
   ```

2. **复制Python脚本**
   ```bash
   # 已包含在项目中
   scripts/ai-bot/extract_activity.py
   scripts/ai-bot/validate_activity.py
   scripts/ai-bot/requirements.txt
   ```

3. **配置GitHub Secrets**（如需要额外权限）
   - 通常不需要，默认使用`GITHUB_TOKEN`

4. **提交到仓库**
   ```bash
   git add .
   git commit -m "feat: 添加AI Bot自动活动整理系统"
   git push
   ```

5. **启用GitHub Actions**
   - 进入 Settings → Actions → General
   - 确保"Allow all actions and reusable workflows"已选中

**完成！** 现在可以在Issues中使用Bot了。

---

## 🔧 环境配置

### Python依赖

Bot需要以下Python包（GitHub Actions已预装Python）：

```bash
pip install -r scripts/ai-bot/requirements.txt
```

**主要依赖：**

| 包名 | 版本 | 用途 |
|------|------|------|
| PyYAML | >=2.0 | YAML文件处理 |
| requests | >=2.31 | HTTP请求 |
| Pillow | >=10.0 | 图像处理（用于future OCR） |
| pydantic | >=2.0 | 数据验证 |

### 本地开发环境

如要在本地测试Bot：

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 安装依赖
pip install -r scripts/ai-bot/requirements.txt

# 设置环境变量
export GITHUB_TOKEN="your-token-here"
export GITHUB_MODELS_API_KEY="your-models-api-key"
export ACTIVITY_URL="https://example.com"
export ACTIVITY_CATEGORY="activity"
export ISSUE_NUMBER="123"

# 运行脚本
python scripts/ai-bot/extract_activity.py
```

---

## 🔑 GitHub Models API设置

### 获取API密钥

1. **访问GitHub Models**
   - 前往 https://github.com/marketplace/models

2. **选择Claude模型**
   - 查看 claude-3-5-sonnet 或其他可用模型

3. **获取API密钥**
   - 个人设置 → Developer settings → Personal access tokens
   - 复制或生成新token（至少需要`public_repo`权限）

### 配置API密钥

**方式一：使用默认的GITHUB_TOKEN（推荐）**

```yaml
# .github/workflows/activity-extractor-bot.yml
env:
  GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  GITHUB_MODELS_API_KEY: ${{ secrets.GITHUB_TOKEN }}
```

GitHub Actions自动提供`GITHUB_TOKEN`，无需手动配置。

**方式二：使用自定义密钥**

1. 生成GitHub Personal Access Token
2. 在仓库Settings → Secrets and variables → Actions中添加：
   - 名称：`GITHUB_MODELS_API_KEY`
   - 值：你的token

3. 在工作流中引用：
   ```yaml
   env:
     GITHUB_MODELS_API_KEY: ${{ secrets.GITHUB_MODELS_API_KEY }}
   ```

### 免费额度

GitHub Models API提供免费额度：
- 具体限额见 https://docs.github.com/en/github-models
- 一般情况下足以支持项目的活动整理需求

### 更换模型

如要使用不同的Claude版本：

```python
# scripts/ai-bot/extract_activity.py

class ActivityExtractor:
    def __init__(self):
        # 修改这一行
        self.model_name = "claude-3-5-sonnet"  # 可改为 claude-3-opus, claude-3-haiku 等
```

可用模型列表：
- `claude-3-5-sonnet` - 推荐，精准度最高
- `claude-3-opus` - 功能最强
- `claude-3-haiku` - 最快（但精度稍低）

---

## ⚙️ 工作流配置

### 工作流文件结构

```
.github/
├── workflows/
│   └── activity-extractor-bot.yml      # 主工作流
├── ISSUE_TEMPLATES/
│   ├── add-activity-ai-bot.md          # AI Bot方式模板
│   └── add-activity-manual.md          # 手动方式模板
└── pull_request_template.md            # PR模板（可选）
```

### 工作流触发条件

```yaml
on:
  issue_comment:
    types: [created, edited]
```

监听条件：
- ✅ Issue中新增评论
- ✅ Issue中编辑现有评论
- ✅ 包含 `@activity-bot extract` 命令

### 权限配置

```yaml
permissions:
  issues: write      # 创建/编辑Issue评论
  contents: read     # 读取仓库内容
  pull-requests: write  # 创建PR
```

### 工作流活动

#### 任务1：extract-activity
触发条件：`@activity-bot extract <URL>`

流程：
1. 检出代码
2. 安装Python环境
3. 解析Issue评论获取URL
4. 调用extract_activity.py
5. 返回结果评论

#### 任务2：create-pull-request
触发条件：`@activity-bot confirm`

流程：
1. 读取ai-bot-results.json
2. 更新对应的YAML文件
3. 创建Pull Request
4. 设置自动删除分支

---

## 🧪 测试和调试

### 本地测试

1. **测试提取脚本**
   ```bash
   export ACTIVITY_URL="https://summer-ospp.ac.cn"
   export ACTIVITY_CATEGORY="competition"
   python scripts/ai-bot/extract_activity.py
   ```

2. **检查输出**
   ```bash
   cat ai-bot-results.json
   ```

3. **验证YAML**
   ```bash
   python scripts/ai-bot/validate_activity.py data/activities.yml
   ```

### 在GitHub Actions中调试

1. **查看运行日志**
   - 进入仓库 → Actions → 选择工作流
   - 点击具体的运行记录
   - 展开步骤查看详细输出

2. **启用调试模式**
   在仓库Secrets中添加：
   - 名称：`ACTIONS_STEP_DEBUG`
   - 值：`true`

3. **常见问题日志**
   ```
   # API连接失败
   "error": "Failed to connect to GitHub Models API"
   
   # 认证失败
   "error": "401 Unauthorized"
   
   # URL无法访问
   "error": "Failed to fetch..."
   ```

### 测试检查清单

- [ ] Bot能否正确解析Issue评论中的URL
- [ ] Bot能否访问测试URL并提取内容
- [ ] AI能否生成有效的JSON
- [ ] JSON能否正确转换为YAML
- [ ] ID能否检测重复
- [ ] 标签能否正确规范化
- [ ] PR能否自动创建

---

## 🔍 故障排除

### Bot没有响应

**原因1：命令格式不正确**
```
❌ @activity-bot extract-activity https://example.com
❌ @activity-bot extract  https://example.com  (多个空格)
✅ @activity-bot extract https://example.com
```

**原因2：GitHub Actions未启用**
- 检查 Settings → Actions → General
- 确保"Allow all actions"已启用

**原因3：工作流文件有语法错误**
- 检查 Actions → 查看错误信息
- 验证YAML语法：https://www.yamllint.com/

### API连接失败

**原因：网络或认证问题**

```bash
# 检查token是否有效
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://models.inference.ai.azure.com/chat/completions

# 查看GitHub Models API状态
# https://github.com/marketplace/models
```

### 提取信息不准确

**常见情况：**
1. **网页内容复杂** - Bot可能混淆信息
   - 尝试提供更清洁的URL（如官方页面而非新闻转载）

2. **多语言内容** - Bot可能优先提取非中文
   - 在命令中补充说明：`@activity-bot extract https://example.com activity Chinese`

3. **JavaScript渲染内容** - 无法抓取动态加载的内容
   - 提供包含静态内容的链接

**解决方案：**
```
在Issue中回复：
- 指出具体错误信息
- 提供正确的信息或替代链接
- 请求Bot重新提取或手动修改
```

### ID冲突

**错误信息：**
```
Event ID 'ospp2025' 已存在于 competitions.yml
```

**解决方案：**
- Bot会自动生成唯一ID（添加-1, -2等后缀）
- 或在Issue中建议新的ID名称

### YAML验证失败

**运行验证脚本：**
```bash
python scripts/ai-bot/validate_activity.py data/activities.yml
```

**常见错误：**
```
❌ 缺少必需字段: title
❌ 字段 deadline 类型错误: 期望 string，得到 int
❌ 无效的ISO 8601时间格式
```

---

## 📊 监控和维护

### 定期检查

1. **每月检查一次：**
   - Bot提取的准确率
   - 是否有新的标签创建需求
   - API使用量是否接近限额

2. **每季度审查：**
   - 提取失败的URL模式
   - 用户反馈和建议
   - 是否需要更新提示词

### 日志分析

查看Actions运行历史：
```bash
# 列出最近的工作流运行
gh run list --limit 10

# 查看特定运行的详情
gh run view <run-id> --log
```

### 性能优化

如果提取变慢：

1. **检查API响应时间**
   - 增加timeout值（当前30秒）

2. **简化提示词**
   - 减少不必要的指令

3. **考虑缓存**
   - 对常见URL进行预处理

---

## 🔐 安全考虑

### Token安全

- ✅ 使用GitHub Actions自动提供的`GITHUB_TOKEN`
- ✅ 不在工作流文件中硬编码token
- ✅ 定期轮换Personal Access Tokens
- ⚠️ 避免在日志中暴露敏感信息

### 数据隐私

- ✅ 仅处理公开URL中的数据
- ✅ 不存储个人信息
- ✅ 所有处理都在GitHub基础设施内

### 审核机制

- ✅ Maintainer最终审核所有PR
- ✅ Bot生成的数据必须人工验证
- ✅ 异常提取结果会被标记

---

## 📚 相关资源

- [GitHub Actions文档](https://docs.github.com/en/actions)
- [GitHub Models API](https://docs.github.com/en/github-models)
- [Claude API文档](https://docs.anthropic.com/)
- [YAML教程](https://yaml.org/spec/)
- [ISO 8601日期时间](https://en.wikipedia.org/wiki/ISO_8601)
- [IANA时区数据库](https://www.iana.org/time-zones)

---

## 💡 常见自定义需求

### 修改提示词

编辑 `scripts/ai-bot/extract_activity.py`，找到 `extraction_prompt` 变量：

```python
extraction_prompt = f"""你的自定义提示词..."""
```

### 添加新的验证规则

编辑 `scripts/ai-bot/validate_activity.py`，在 `validate_activity_data` 方法中添加：

```python
def validate_activity_data(self, data: Dict) -> Tuple[bool, List[str], List[str]]:
    # 添加你的验证逻辑
    if your_condition:
        self.errors.append("你的错误信息")
```

### 修改YAML生成格式

编辑 `scripts/ai-bot/extract_activity.py` 中的 `extract` 方法：

```python
yaml_data = {
    # 自定义你的字段
}
```

---

**最后更新**：2025年1月  
**维护者**：[@your-github-username]
