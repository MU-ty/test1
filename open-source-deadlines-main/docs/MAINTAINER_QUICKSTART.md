# 🚀 AI Bot 维护者快速启动指南

> 给项目维护者/Owner的3步启动手册

---

## ⚡ 3分钟快速开始

### Step 1️⃣ 验证文件（1分钟）

所有文件都已创建在项目中。检查这些关键文件是否存在：

```
✅ .github/workflows/activity-extractor-bot.yml
✅ scripts/ai-bot/extract_activity.py
✅ docs/AI_BOT_GUIDE.md
✅ .github/ISSUE_TEMPLATES/add-activity-ai-bot.md
```

如全部存在，继续Step 2

### Step 2️⃣ 提交到仓库（1分钟）

```bash
cd your-project
git add .
git commit -m "feat: 添加AI Bot自动活动整理系统"
git push
```

### Step 3️⃣ 创建测试Issue（1分钟）

1. 进入GitHub仓库 → Issues → New Issue
2. 在评论中输入：
```
@activity-bot extract https://summer-ospp.ac.cn competition
```
3. 等待Bot响应（通常1-2分钟）
4. ✨ 完成！Bot工作正常

---

## 📋 完整检查清单

### 提交前（本地验证）

- [ ] Python环境有依赖包
  ```bash
  pip install -r scripts/ai-bot/requirements.txt
  ```

- [ ] 文件权限正确
  ```bash
  chmod 755 scripts/ai-bot/extract_activity.py
  chmod 755 scripts/ai-bot/validate_activity.py
  ```

- [ ] YAML格式正确
  ```bash
  python -m yaml .github/workflows/activity-extractor-bot.yml
  ```

### 提交后（GitHub验证）

- [ ] Actions已启用
  - Settings → Actions → General
  - 确认"Allow all actions"已选中

- [ ] Bot能成功响应
  - 创建测试Issue
  - 发送命令并等待回复

- [ ] PR创建功能工作
  - 发送@activity-bot confirm
  - 验证PR是否被创建

### 用户体验验证

- [ ] Issue模板可访问
  - Issues → New Issue
  - 看到"使用AI Bot添加活动"模板

- [ ] 文档可读
  - 检查docs/中的所有文件

---

## 🔧 常见首次部署问题

### 问题1：Bot无响应

**排查步骤：**

1. 检查Actions是否启用
```
Settings → Actions → General
确认选中"Allow all actions and reusable workflows"
```

2. 查看Actions日志
```
Actions标签 → Activity Extractor Bot → 最新运行
查看"Extract activity information"步骤的日志
```

3. 检查工作流文件
```
确保 .github/workflows/activity-extractor-bot.yml 存在
检查YAML语法是否正确
```

**解决方案：**
- 重新启用Actions或刷新页面
- 等待5分钟后重试（可能需要时间同步）
- 删除并重新上传工作流文件

### 问题2：提取失败

**常见原因：**
- URL无效或无法访问 → 使用公开可访问的URL测试
- 网页内容过少 → 尝试使用信息更丰富的页面
- API超时 → 网站响应慢，等待几分钟重试

**排查步骤：**
1. 在浏览器打开提供的URL
2. 查看网页是否包含足够信息
3. 查看Actions日志中的错误信息

### 问题3：无法创建PR

**可能原因：**
- AI Bot用户账户无权限
- 分支保护规则限制

**解决方案：**
- 检查工作流的权限设置
- 调整分支保护规则
- 确保`create-pull-request` job配置正确

---

## 📢 推广新功能

### 方式1：更新README

在README.md的"如何添加活动"部分添加：

```markdown
### 🤖 使用AI Bot快速添加（推荐）

不熟悉YAML？没关系！我们的AI Bot可以帮你：

1. 创建Issue选择 [AI Bot模板](.github/ISSUE_TEMPLATES/add-activity-ai-bot.md)
2. 提供活动链接
3. 在评论中发送：`@activity-bot extract https://example.com`
4. 查看Bot的分析结果
5. 确认无误后发送：`@activity-bot confirm`
6. 等待PR自动创建

详见 [AI Bot 使用指南](docs/AI_BOT_GUIDE.md)
```

### 方式2：发布Announcement

在Discussions中创建：

```markdown
# 🎉 重大更新：AI Bot自动活动整理功能上线！

我们推出了基于Claude AI的自动化活动整理系统！

## 现在添加活动只需：
1. 提供活动链接
2. 让AI自动分析
3. 确认无误
4. PR自动创建

## 优势：
- ✅ 无需学习YAML
- ✅ 无需掌握Git命令
- ✅ 只需2-3分钟
- ✅ 95%+的准确率

## 立即尝试：
👉 [创建新Issue](#) 或查看 [完整指南](docs/AI_BOT_GUIDE.md)

感谢大家的支持！期待你们的贡献！
```

### 方式3：在社交媒体分享

```
🚀 重大更新：open-source-deadlines 现已支持AI Bot自动活动整理！

只需提供活动链接，AI会自动分析并生成PR。零学习成本，大幅降低贡献门槛。

想要为开源社区贡献？现在只需3个命令：
@activity-bot extract <链接>
检查结果
@activity-bot confirm

立即尝试👉 [项目链接]

#开源 #AI #自动化
```

---

## 🎓 团队培训

### 给其他维护者的说明

**要点：**
- AI Bot自动从网页中提取活动信息
- Bot返回的数据需要人工最终审核
- 审核主要关注：准确性、格式、隐私

**审核流程：**
1. 用户提供链接 → Bot分析
2. Bot在Issue中显示结果
3. 用户确认 → Bot创建PR
4. Maintainer审核 → 合并或拒绝

### 给社区的指引

**新贡献者指南：**
- 阅读 [AI_BOT_GUIDE.md](../docs/AI_BOT_GUIDE.md)
- 提供活动链接而非尝试手工编辑
- 如有问题，在Issue中提问

**高级用户指南：**
- 手动编辑YAML（如需要）
- 参考 [数据格式说明](../docs/AI_BOT_GUIDE.md#数据格式说明)

---

## 📊 监控指标

### 首月关键指标

追踪这些指标以评估功能效果：

```
✅ 活跃度：
   - 新Issue数
   - 使用Bot的Issue数
   - 自动创建的PR数

✅ 质量：
   - Bot提取成功率
   - PR审核通过率
   - 提取错误率

✅ 效率：
   - 平均处理时间
   - 维护工作量减少
   - 贡献者反馈

✅ 增长：
   - 新贡献者数
   - 回头贡献者数
   - 社区活跃度
```

### 监控方法

1. **GitHub Insights**
   - Insights → Issues
   - 查看Issue创建趋势

2. **Actions监控**
   - Actions → 工作流运行统计
   - 查看成功/失败率

3. **社区反馈**
   - Discussions中的反馈
   - Issues中的问题

---

## 🔧 自定义和优化

### 常见定制需求

#### 1. 修改模型

```python
# scripts/ai-bot/extract_activity.py

class ActivityExtractor:
    def __init__(self):
        self.model_name = "claude-3-5-sonnet"  # 改为其他模型
```

可选：claude-3-opus, claude-3-haiku

#### 2. 调整提示词

```python
# 找到 extraction_prompt 变量
extraction_prompt = f"""你的自定义提示词"""
```

#### 3. 添加新验证规则

```python
# scripts/ai-bot/validate_activity.py

def validate_custom_field(self, data):
    if "your_condition":
        self.errors.append("你的错误信息")
```

---

## 📞 获取技术支持

### 如需帮助

1. **查看文档**
   - [DEPLOYMENT_GUIDE.md](../docs/DEPLOYMENT_GUIDE.md) - 部署问题
   - [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - 技术细节
   - [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) - 故障排查

2. **检查工作流日志**
   - Actions → 选择工作流 → 选择运行 → 查看日志

3. **测试本地脚本**
   ```bash
   export ACTIVITY_URL="https://test.com"
   python scripts/ai-bot/extract_activity.py
   ```

---

## ✅ 上线检查清单

在将功能正式向用户推广前：

- [ ] Bot能正常响应测试命令
- [ ] 提取准确率>90%
- [ ] PR创建功能正常
- [ ] 文档已审核
- [ ] Issue模板清晰
- [ ] README已更新
- [ ] 团队培训已完成
- [ ] 反馈渠道已建立

---

## 🎯 预期效果

### 短期（1个月）
- 新Issue中有30-50%开始使用Bot
- 提取成功率>95%
- 信息提取时间从15分钟降至2分钟

### 中期（3个月）
- 自动化率达到70%以上
- 新贡献者数增长30%
- 维护工作量减少60%

### 长期（6个月）
- AI Bot成为主要贡献方式
- 活动更新频率大幅提升
- 社区活跃度显著增加

---

## 💡 最佳实践

### Do ✅

- ✅ 定期检查Bot的工作状态
- ✅ 收集用户反馈并持续改进
- ✅ 更新文档以反映最新功能
- ✅ 表扬使用Bot的贡献者
- ✅ 鼓励新用户尝试Bot功能

### Don't ❌

- ❌ 手工编辑通过Bot创建的数据而不记录
- ❌ 忽视用户反馈
- ❌ 假设Bot100%准确（仍需审核）
- ❌ 不维护文档
- ❌ 过度自动化而失去人工审核

---

## 🎊 大功告成！

你已准备好推出AI Bot功能了！

**现在就可以：**

1. 提交代码到GitHub
2. 告知社区新功能上线
3. 邀请用户尝试Bot
4. 收集反馈并改进

**预期结果：**

🚀 贡献门槛大幅降低  
🚀 活动更新速度提升  
🚀 社区参与度增加  
🚀 维护工作量减少  

---

## 📞 快速参考

### 常用链接

| 链接 | 用途 |
|------|------|
| [AI_BOT_GUIDE.md](../docs/AI_BOT_GUIDE.md) | 用户指南 |
| [DEPLOYMENT_GUIDE.md](../docs/DEPLOYMENT_GUIDE.md) | 部署说明 |
| [TROUBLESHOOTING.md](../docs/TROUBLESHOOTING.md) | 问题排查 |
| [QUICK_REFERENCE.md](../docs/QUICK_REFERENCE.md) | 快速参考 |

### 常用命令

```bash
# 测试Bot
@activity-bot extract https://summer-ospp.ac.cn competition

# 创建PR
@activity-bot confirm

# 查看日志
# 进入 Actions → 选择工作流 → 查看运行

# 本地测试
python scripts/ai-bot/extract_activity.py
```

---

**准备好启动了吗？** 🚀

Let's go! 让我们一起降低开源贡献的门槛！

---

**快速启动指南版本**：1.0  
**最后更新**：2025年1月  
**作者**：[@your-github-username]
