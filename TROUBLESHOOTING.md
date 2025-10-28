# 🔧 AI Bot 故障排查指南

## 问题：Bot 没有在 Issue 中回复

### 🔍 可能的原因和解决方案

---

## ❌ 原因 1: GH_MODELS_TOKEN Secret 未配置

### 症状
- Bot 没有任何回复
- GitHub Actions 日志中看不到运行记录

### 解决方案

**Step 1: 创建 GitHub Personal Token**

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 填写信息：
   - **Note**: `AI Bot - GitHub Models`
   - **Expiration**: 90 days
   - **Scopes**: 选择 `repo` 和 `read:org`
4. 点击 **Generate token**
5. **立即复制** token（只显示一次！）

**Step 2: 添加到仓库 Secrets**

1. 进入仓库 → **Settings**
2. 左侧菜单 → **Secrets and variables** → **Actions**
3. 点击 **New repository secret**
4. 填写：
   - **Name**: `GH_MODELS_TOKEN`
   - **Value**: 粘贴刚才复制的 token
5. 点击 **Add secret**

✅ **完成！** Secret 已配置

**Step 3: 重新测试**

在 Issue 中再次输入：
```
@activity-bot extract https://competition.atomgit.com/competition
```

等待 1-2 分钟，Bot 应该会回复。

---

## ❌ 原因 2: GitHub Actions 权限不足

### 症状
- Actions 标签页看不到工作流运行
- 或者工作流运行但权限不足

### 解决方案

1. 进入仓库 → **Settings**
2. 左侧菜单 → **Actions** → **General**
3. 找到 **Workflow permissions** 部分
4. 选择 **Read and write permissions**
5. ✅ 勾选 **Allow GitHub Actions to create and approve pull requests**
6. 点击 **Save**

---

## ❌ 原因 3: 工作流文件语法错误

### 症状
- Actions 页面显示红色错误
- 工作流无法运行

### 解决方案

**检查工作流文件**

1. 打开 `.github/workflows/ai-bot-handler.yml`
2. 验证文件格式：
   - 不能有 Tab 字符（只能用空格）
   - YAML 缩进必须正确
   - 所有冒号后面要有空格

**常见错误**:
```yaml
# ❌ 错误：没有空格
run:python scripts/ai-bot/bot_handler.py extract

# ✅ 正确：
run: python scripts/ai-bot/bot_handler.py extract
```

**在线验证**：
使用 https://www.yamllint.com/ 验证 YAML 语法

---

## ❌ 原因 4: 工作流未被触发

### 症状
- Issue 有评论，但 Actions 页面没有运行记录

### 解决方案

**检查工作流触发条件**

工作流应该在 Issue 评论时自动触发：

```yaml
on:
  issue_comment:
    types: [created, edited]
```

**手动测试触发**：

1. 进入仓库 → **Actions**
2. 找到 **ai-bot-handler** workflow
3. 点击 **Run workflow**
4. 选择分支：**main**
5. 点击 **Run workflow**

如果手动运行成功，说明工作流配置正确。

---

## ❌ 原因 5: 命令格式不正确

### 症状
- Bot 没有回复
- 或者回复错误信息

### 解决方案

**检查命令格式**

正确的格式：
```
@activity-bot extract <URL> [category]
```

**有效的例子**:
```
@activity-bot extract https://competition.atomgit.com/competition
@activity-bot extract https://github.com/features activity
@activity-bot extract https://pycon.org conference
```

**常见错误**:
```
❌ @activitybot extract ...        (错误：activitybot)
❌ @activity bot extract ...       (错误：activity bot)
❌ @activity-bot EXTRACT ...       (错误：大写)
❌ activity-bot extract ...        (错误：缺少 @)
```

---

## 📋 完整的故障排查检查清单

按顺序检查：

### ✅ Step 1: 验证 Secret 配置
```
Settings → Secrets and variables → Actions
是否看到 GH_MODELS_TOKEN？
```

### ✅ Step 2: 验证工作流文件
```
.github/workflows/ai-bot-handler.yml 是否存在？
```

### ✅ Step 3: 验证 Python 文件
```
scripts/ai-bot/ 中是否有所有必需的 .py 文件？
```

### ✅ Step 4: 验证命令格式
```
在 Issue 中输入的命令是否正确？
```

### ✅ Step 5: 检查 Actions 日志
```
1. 进入 Actions 标签
2. 点击最新的运行
3. 查看完整的错误日志
```

---

## 🐛 查看 GitHub Actions 日志

这是最有效的调试方法：

**Step 1: 打开 Actions**
- 进入仓库主页
- 点击上方 **Actions** 标签

**Step 2: 查看最近的运行**
- 找到最近的 workflow 运行
- 点击进去

**Step 3: 查看详细日志**
- 点击 **handle-bot-command** job
- 展开各个 step 查看输出
- 重点看 "Run Python handler" step

**Step 4: 关键信息**
- 查找 "Error" 或 "error" 关键词
- 查看 Python 错误堆栈
- 记录具体错误信息

---

## 💡 常见错误信息及解决方案

### 错误 1: "缺少 GH_MODELS_TOKEN"
```
Error: GH_MODELS_TOKEN environment variable not found
```
**解决**: 配置 Secret，参见上方步骤

### 错误 2: "API 调用失败"
```
Error: API call failed: 401 Unauthorized
```
**解决**: 
- Token 已过期或无效
- 重新生成 token
- 更新 Secret

### 错误 3: "网页爬取失败"
```
Error: Failed to fetch page: Connection timeout
```
**解决**: 
- 网站可能不可访问
- 尝试其他 URL
- 检查网络连接

### 错误 4: "JSON 解析失败"
```
Error: JSON decode error
```
**解决**: 
- AI 返回的格式错误
- 检查网页内容是否足够
- 尝试其他网页

---

## ✅ 验证系统是否正常工作

### 快速测试

**创建一个新 Issue，标题: "AI Bot Test"，内容:**

```
@activity-bot extract https://github.com/features activity
```

**预期结果 (1-2分钟内)**:

✅ Bot 在 Issue 中回复：
```
✓ 提取成功！

标题: GitHub Features
描述: Learn about GitHub's latest features...
...
```

❌ 如果没有回复，检查：
1. 是否看到 Actions 运行？
2. 运行是否成功？
3. 是否有错误日志？

---

## 🆘 还是不行？

### 最后的诊断步骤

1. **清空日志，重新测试**
   ```
   删除之前的 Issue 注释
   重新输入命令
   等待新的运行
   ```

2. **检查完整的 Actions 日志**
   ```
   Actions → 最近的运行 → 点击job
   查看完整的运行日志
   复制错误信息
   ```

3. **验证代码完整性**
   ```
   scripts/ai-bot/
   ├── bot_handler.py     ✅
   ├── web_scraper.py     ✅
   ├── ai_analyzer.py     ✅
   ├── data_validator.py  ✅
   ├── utils.py           ✅
   └── requirements.txt   ✅
   ```

4. **尝试手动运行工作流**
   ```
   Actions → ai-bot-handler → Run workflow
   选择 main 分支
   点击 Run workflow
   ```

---

## 📞 获取更多帮助

- 📖 查看 `QUICKSTART.md` 
- 📖 查看 `AI_BOT_USAGE_GUIDE.md`
- 📖 查看 `DEPLOYMENT_CHECKLIST.md`
- 🔗 查看 GitHub Actions 官方文档

---

## ⚡ 快速解决方案总结

| 问题 | 解决方案 | 时间 |
|------|---------|------|
| 没有回复 | 配置 GH_MODELS_TOKEN | 5分钟 |
| Actions 权限 | 设置为 "Read and write" | 1分钟 |
| 工作流错误 | 检查 YAML 语法 | 5分钟 |
| 命令格式 | 使用 @activity-bot extract URL | 1分钟 |
| API 失败 | 检查 token 是否有效 | 5分钟 |

**99% 的问题都是因为 GH_MODELS_TOKEN 未配置！** ✅

---

**现在立即检查并配置 Secret，Bot 就会开始工作！** 🚀
