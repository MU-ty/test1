# ⚡ Bot 没有回复？快速修复 (5分钟)

## 🎯 最可能的原因

**99% 的情况是**: `GH_MODELS_TOKEN` Secret 没有配置！

---

## ✅ 立即修复 (只需 5分钟)

### Step 1️⃣: 获取 Token (2分钟)

在浏览器打开此链接：
```
https://github.com/settings/tokens
```

1. 点击绿色的 **Generate new token (classic)** 按钮

2. 填写表单：
   ```
   Note: AI Bot - GitHub Models
   Expiration: 90 days
   ```

3. 向下滚动，在 **Scopes** 部分：
   - ✅ 勾选 `repo` (所有)
   - ✅ 勾选 `read:org`

4. 点击底部绿色 **Generate token** 按钮

5. **重要**: 立即复制显示的 token
   - 它只会显示一次！
   - 复制到剪贴板

---

### Step 2️⃣: 添加到仓库 (2分钟)

1. 打开你的仓库页面
2. 点击上方 **Settings** (设置)
3. 左侧菜单找到 **Secrets and variables**
4. 点击 **Actions**
5. 点击绿色的 **New repository secret** 按钮

6. 填写：
   ```
   Name: GH_MODELS_TOKEN
   Value: [粘贴刚才复制的 token]
   ```

7. 点击 **Add secret**

✅ **完成！**

---

### Step 3️⃣: 重新测试 (1分钟)

在你的 Issue #1 中，再次输入：

```
@activity-bot extract https://competition.atomgit.com/competition
```

**等待 1-2 分钟**，Bot 应该会回复！

---

## 🔍 如果还是没有回复

### 检查 1: Actions 权限

1. Settings → **Actions** → **General**
2. 找到 **Workflow permissions**
3. 选择 **Read and write permissions**
4. ✅ 勾选 "Allow GitHub Actions to create and approve pull requests"
5. **Save**

### 检查 2: 查看 Actions 日志

1. 点击仓库上方的 **Actions** 标签
2. 左侧找到 **ai-bot-handler** workflow
3. 点击最新的运行记录
4. 查看错误信息

### 检查 3: 命令格式

确保命令格式正确：
```
✅ @activity-bot extract https://example.com
❌ @activitybot extract https://example.com
❌ activity-bot extract https://example.com
```

---

## 📊 验证清单

- [ ] 已访问 https://github.com/settings/tokens
- [ ] 已创建 Personal Token (并复制)
- [ ] 已进入仓库 Settings
- [ ] 已进入 Secrets and variables → Actions
- [ ] 已创建名为 `GH_MODELS_TOKEN` 的 secret
- [ ] 已粘贴 token 值
- [ ] 已点击 "Add secret"
- [ ] 已在 Issue 中重新输入命令
- [ ] 等待了 1-2 分钟

---

## 💡 问题排查

| 症状 | 解决方案 |
|------|---------|
| 完全没有回复 | 配置 GH_MODELS_TOKEN secret |
| Actions 显示错误 | 检查权限设置为 "Read and write" |
| API 返回 401 | Token 无效，重新生成 |
| 网页爬取失败 | 尝试其他 URL |

---

## ✨ 预期结果

正确配置后，Bot 会在 Issue 中回复类似这样的内容：

```
✓ 提取成功！

标题: AtomGit Programming Competition
描述: A programming competition platform...
开始日期: 2024-01-01
结束日期: 2024-12-31
地点: Online
标签: [programming, competition, coding]
来源: https://competition.atomgit.com/competition
```

然后你可以输入：
```
@activity-bot confirm
```

Bot 会创建一个 Pull Request！

---

## 🆘 还有问题？

查看完整的故障排查指南：
- 📖 `TROUBLESHOOTING.md` - 详细的问题排查
- 📖 `QUICKSTART.md` - 快速启动指南
- 📖 `AI_BOT_USAGE_GUIDE.md` - 完整使用说明

---

**立即配置，Bot 马上就能工作！** 🚀
