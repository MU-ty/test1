# GitHub Models API 集成指南

本指南说明如何配置和使用 GitHub Models API 与 AI Bot 系统集成。

## 什么是 GitHub Models？

GitHub Models 是 GitHub 提供的托管 AI 模型服务，允许开发者通过 GitHub 账户免费使用多个先进的 AI 模型，包括：

- **Claude 3.5 Sonnet** - 多模态模型，适合复杂分析任务
- **GPT-4o** - OpenAI 最新模型
- **Mistral Large** - 开源模型
- 更多模型...

## 为什么使用 GitHub Models？

✅ **免费** - 开发时无成本  
✅ **集成** - 直接使用 GitHub Token  
✅ **可靠** - GitHub 官方服务  
✅ **便捷** - 无需额外注册

## 获取 API Token

### 步骤1：创建 Personal Access Token

1. 访问 https://github.com/settings/tokens
2. 点击 **Generate new token (classic)**
3. 填写 Token 信息：
   - **Note**: "AI Bot - GitHub Models"
   - **Expiration**: 建议 90 天（定期更新）
   - **Scopes**: 选择 `repo` 和 `read:org`

4. 点击 **Generate token**
5. 复制生成的 token（稍后需要）

### 步骤2：配置仓库 Secret

1. 进入仓库 → **Settings** → **Secrets and variables** → **Actions**
2. 点击 **New repository secret**
3. 创建 secret：
   - **Name**: `GH_MODELS_TOKEN`
   - **Value**: 粘贴刚才复制的 token
4. 点击 **Add secret**

## API 调用格式

### 请求示例

```python
import requests

token = "github_pat_XXXXX"  # 你的 GH_MODELS_TOKEN
url = "https://models.inference.ai.azure.com/chat/completions"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "model": "gpt-4o-mini",  # 或其他可用模型
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful assistant."
        },
        {
            "role": "user",
            "content": "Analyze this webpage content..."
        }
    ],
    "temperature": 0.7,
    "max_tokens": 500
}

response = requests.post(url, headers=headers, json=payload)
result = response.json()
```

### 可用模型

| 模型 | 推荐用途 | 成本 |
|------|---------|------|
| `gpt-4o-mini` | 快速分析（**AI Bot使用**） | 免费 |
| `claude-3.5-sonnet` | 复杂分析 | 免费 |
| `mistral-large` | 多语言 | 免费 |

## AI Bot 中的 API 集成

### 在 `ai_analyzer.py` 中的实现

```python
class ActivityAnalyzer:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = "gpt-4o-mini"
        self.api_url = "https://models.inference.ai.azure.com/chat/completions"
    
    def analyze(self, text: str, category: str, url: str) -> dict:
        # 构建提示词
        prompt = self._build_prompt(text, category, url)
        
        # 调用 API
        response = self._call_api(prompt)
        
        # 解析结果
        return response
```

### 环境变量配置

GitHub Actions 工作流会自动设置：

```yaml
env:
  GH_MODELS_TOKEN: ${{ secrets.GH_MODELS_TOKEN }}
```

Python 脚本通过以下方式获取：

```python
import os
api_key = os.getenv('GH_MODELS_TOKEN')
```

## 故障排查

### 问题1：401 Unauthorized

**症状**: API 返回 401 错误

**原因**:
- Token 无效或已过期
- Token 权限不足

**解决方案**:
1. 重新生成 token
2. 确保 token 在仓库 Secrets 中正确配置
3. 检查 token 过期时间

### 问题2：429 Too Many Requests

**症状**: API 返回 429 错误

**原因**: 请求过于频繁（超过速率限制）

**解决方案**:
1. 减少并发请求数量
2. 添加请求间隔（retry with backoff）
3. 使用缓存避免重复请求

### 问题3：模型不可用

**症状**: 返回 "model not found" 错误

**原因**: 模型名称错误或该模型不可用

**解决方案**:
1. 检查模型名称是否正确
2. 切换到其他可用模型
3. 访问 https://github.com/marketplace/models 查看可用模型列表

## 最佳实践

### 1. 错误处理

```python
try:
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    logger.error(f"API call failed: {str(e)}")
    # 实现 fallback 策略
```

### 2. 请求超时

```python
# 设置合理的超时时间（秒）
response = requests.post(url, timeout=30)
```

### 3. 响应验证

```python
# 验证响应格式
result = response.json()
if 'choices' not in result:
    raise ValueError("Invalid response format")

message = result['choices'][0]['message']['content']
```

### 4. 成本监控

```python
# 记录 API 使用情况
logger.info(f"Model: {model}, Tokens: {usage['total_tokens']}")
```

## 升级到付费 API（可选）

如需使用 OpenAI、Claude 等付费服务，只需：

1. 在各服务获取 API Key
2. 修改 `ai_analyzer.py` 中的 API 端点和认证方式
3. 更新 environment variables
4. 配置成本告警

### 示例：使用 OpenAI API

```python
# 修改 API 端点
self.api_url = "https://api.openai.com/v1/chat/completions"
self.headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}
```

## 监控和日志

### 查看 API 使用情况

在 GitHub Actions 运行日志中查看：

```
INFO: API call started (model: gpt-4o-mini)
INFO: Response received: 245 tokens
INFO: Analysis completed successfully
```

### 调试 API 问题

启用详细日志：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 成本估算

使用 GitHub Models（免费）：

- **无限制** - 免费使用配额
- **速率限制** - 取决于 GitHub 政策
- **监控** - 在 GitHub Settings 查看使用情况

## 参考资源

- 📚 [GitHub Models 文档](https://docs.github.com/en/github-models)
- 🔗 [GitHub Marketplace 模型](https://github.com/marketplace/models)
- 📖 [Claude 官方文档](https://docs.anthropic.com/)
- 🌐 [OpenAI API 文档](https://platform.openai.com/docs/)

## 常见问题

**Q: 能否在本地测试 API？**  
A: 可以。只需获取有效的 token 并在本地设置环境变量 `GH_MODELS_TOKEN`。

**Q: Token 泄露了怎么办？**  
A: 立即撤销 token（https://github.com/settings/tokens），然后生成新 token。

**Q: 如何选择合适的模型？**  
A: 对于活动信息提取，`gpt-4o-mini` 速度快且准确，是最佳选择。

---

**最后更新**: 2024年  
**版本**: 1.0  
**状态**: 生产就绪
