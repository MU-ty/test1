# AI Bot 快速启动指南

完成以下步骤即可在合并后立即使用 AI Bot 系统：

## 第一步：配置 GitHub Secrets

1. 进入你的仓库：**Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 创建以下密钥：

| 密钥名称 | 值 | 说明 |
|---------|-----|------|
| `GH_MODELS_TOKEN` | 你的GitHub Personal Token | 用于调用GitHub Models API |

### 如何获取 GitHub Personal Token：

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 选择作用域：`repo`, `read:org`
4. 生成并复制 token
5. 粘贴到仓库的 Secrets 中

## 第二步：测试系统

合并PR后，创建一个新Issue来测试AI Bot：

### 测试命令格式：

```
@activity-bot extract <URL> <category>
```

**参数说明：**
- `<URL>`：要爬取的网页链接（必需）
- `<category>`：活动分类，可选值：`activity`, `conference`, `competition`（默认：activity）

### 测试示例：

```
@activity-bot extract https://example.com/event competition
```

## 第三步：确认提取结果

AI Bot 完成提取后，在Issue中回复：

```
@activity-bot confirm
```

系统会自动创建PR，将提取的活动信息添加到相应的YAML文件。

## 第四步：审查和合并PR

1. 查看AI Bot生成的PR
2. 审查提取的活动信息
3. 根据需要进行调整
4. 合并PR

## 功能流程图

```
Issue Comment: @activity-bot extract URL category
    ↓
GitHub Actions Triggered
    ↓
Step 1: 爬取网页内容
    ↓
Step 2: Claude AI分析
    ↓
Step 3: 数据验证
    ↓
Step 4: 生成YAML
    ↓
保存结果到Issue Comment
    ↓
用户确认：@activity-bot confirm
    ↓
创建PR并更新YAML文件
    ↓
完成！
```

## 常见问题

### Q: 提取失败，报错 "缺少GH_MODELS_TOKEN"
**A:** 需要在仓库Secrets中配置GH_MODELS_TOKEN。参见第一步。

### Q: 提取的信息不完整
**A:** 这是正常的。AI有时无法从所有网页中提取完整信息。你可以：
1. 手动编辑提取的结果
2. 或者使用Manual方式提交

### Q: 多长时间会返回结果？
**A:** 通常在1-2分钟内。GitHub Actions会在Issue中回复提取结果。

### Q: 如何修改已生成的PR？
**A:** 直接编辑PR中的文件，或关闭PR后重新提交。

## 支持的活动类型

- **activity**: 一般开源活动、讲座、工作坊等
- **conference**: 技术会议
- **competition**: 编程竞赛

## 故障排查

如果系统出现问题：

1. **检查GitHub Actions日志**
   - 进入仓库 → Actions → 找到失败的运行
   - 查看完整的错误消息

2. **验证文件结构**
   - 确保 `.github/workflows/ai-bot-handler.yml` 存在
   - 确保 `scripts/ai-bot/` 下的所有Python文件都存在

3. **检查权限**
   - 确保GitHub Actions有足够权限创建PR
   - 仓库Settings → Actions → General → Workflow permissions

## 获取帮助

如有问题，请：
1. 查看GitHub Actions日志中的错误信息
2. 查阅本仓库的Issue或Discussion
3. 提交新Issue描述问题

---

**系统已完全配置！现在可以开始使用AI Bot了。** 🚀
