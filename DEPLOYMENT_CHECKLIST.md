# 部署检查清单

完成以下清单确保AI Bot系统正确部署：

## ✅ 代码文件检查

### 核心文件
- [ ] `.github/workflows/ai-bot-handler.yml` 存在
- [ ] `scripts/ai-bot/bot_handler.py` 存在
- [ ] `scripts/ai-bot/web_scraper.py` 存在
- [ ] `scripts/ai-bot/ai_analyzer.py` 存在
- [ ] `scripts/ai-bot/data_validator.py` 存在
- [ ] `scripts/ai-bot/utils.py` 存在
- [ ] `scripts/ai-bot/requirements.txt` 存在
- [ ] `scripts/ai-bot/__init__.py` 存在

### 文档文件
- [ ] `QUICKSTART.md` 存在（本文件）
- [ ] `DEPLOYMENT_CHECKLIST.md` 存在（本文件）

### 现有项目文件
- [ ] `data/activities.yml` 存在
- [ ] `data/conferences.yml` 存在
- [ ] `data/competitions.yml` 存在

## 🔧 GitHub 配置检查

### Secrets 配置
- [ ] 访问 Settings → Secrets and variables → Actions
- [ ] 创建 `GH_MODELS_TOKEN` secret
- [ ] 获取了有效的 GitHub Personal Token

### Actions 权限
- [ ] 进入 Settings → Actions → General
- [ ] Workflow permissions 设置为 "Read and write permissions"
- [ ] 勾选 "Allow GitHub Actions to create and approve pull requests"

### Branch Protection (可选)
- [ ] 如果启用了分支保护，检查AI Bot有权限推送到分支

## 📝 代码质量检查

### Python 语法检查
```bash
# 在项目根目录运行
python -m py_compile scripts/ai-bot/bot_handler.py
python -m py_compile scripts/ai-bot/web_scraper.py
python -m py_compile scripts/ai-bot/ai_analyzer.py
python -m py_compile scripts/ai-bot/data_validator.py
python -m py_compile scripts/ai-bot/utils.py
```

预期结果：没有错误输出

### 依赖检查
```bash
cd scripts/ai-bot
pip install -r requirements.txt
```

预期结果：所有包都成功安装

### 导入检查
```bash
# 在项目根目录运行
python -c "import sys; sys.path.insert(0, 'scripts/ai-bot'); import bot_handler"
```

预期结果：没有 ImportError

## 🧪 功能测试

### 测试1：创建测试Issue
1. 在仓库中创建新Issue
2. 标题：`[AI Bot Test] Testing extraction`
3. 内容：
```
@activity-bot extract https://github.com/features activity
```

预期结果：
- AI Bot 评论中提示正在处理
- 1-2分钟后返回提取结果
- 结果包含 JSON 格式的活动信息

### 测试2：验证数据格式
检查AI Bot返回的数据是否包含：
- [ ] `title`: 活动标题
- [ ] `description`: 活动描述
- [ ] `start_date`: 开始日期
- [ ] `end_date`: 结束日期
- [ ] `location`: 活动地点
- [ ] `tags`: 标签列表
- [ ] `url`: 源网址

### 测试3：confirm 命令测试
1. 在测试Issue中回复：
```
@activity-bot confirm
```

预期结果：
- AI Bot 创建 Pull Request
- PR包含更新的YAML数据
- PR标题包含活动ID和类别

## 🔍 常见问题排查

### 问题：Actions 未运行
**检查项：**
- [ ] `.github/workflows/ai-bot-handler.yml` 文件正确放置
- [ ] 文件名完全匹配（case-sensitive）
- [ ] 工作流文件语法正确（查看 Actions 标签的错误）
- [ ] 仓库已启用 Actions

### 问题：导入错误
**检查项：**
- [ ] 所有依赖已在 `requirements.txt` 中列出
- [ ] Python 版本 >= 3.9
- [ ] 所有模块文件都在 `scripts/ai-bot/` 目录中
- [ ] 没有循环导入

### 问题：API 调用失败
**检查项：**
- [ ] `GH_MODELS_TOKEN` 已正确配置
- [ ] Token 有效且未过期
- [ ] Token 有正确的权限范围
- [ ] GitHub Models API 服务可访问

### 问题：数据验证失败
**检查项：**
- [ ] 日期格式为 YYYY-MM-DD 或 YYYY-MM-DD HH:MM:SS
- [ ] 至少包含一个标签
- [ ] 地点信息非空
- [ ] 结束日期不早于开始日期

## 📊 性能指标

系统正常运行的预期性能：

| 指标 | 预期值 |
|------|--------|
| 网页爬取时间 | 2-5 秒 |
| AI 分析时间 | 10-20 秒 |
| 数据验证时间 | <1 秒 |
| 总处理时间 | 15-30 秒 |
| PR 创建时间 | <5 秒 |

## 🚀 部署验收标准

系统完全就绪的标准：

- [ ] 所有代码文件都正确放置
- [ ] GitHub Secrets 配置完成
- [ ] Actions 权限正确配置
- [ ] 测试Issue能成功提取信息
- [ ] confirm 命令能创建PR
- [ ] 生成的YAML格式正确
- [ ] 文档齐全且准确

## 📞 支持资源

如遇到问题，参考以下资源：

1. **GitHub Actions 文档**: https://docs.github.com/en/actions
2. **GitHub Models API**: https://github.com/marketplace/models
3. **本仓库Issues**: 搜索已有的问题和解决方案
4. **本仓库Discussions**: 提问和讨论

## ✨ 完成

当所有检查项都完成后，系统即可投入使用！

```
┌─────────────────────────────────────┐
│  🎉 AI Bot 系统已完全就绪！ 🎉       │
│                                     │
│  现在可以开始使用 @activity-bot      │
│  命令来自动提取和处理活动信息了。    │
└─────────────────────────────────────┘
```

---

**最后更新**: 2024年
**版本**: 1.0.0
**状态**: 生产就绪
