# AIcosplay (AI人物扮演)

基于 Streamlit 和 DeepSeek API 构建的本地化 AI 角色扮演对话应用。支持高度定制化的人物设定与多任务会话隔离管理。

## 核心功能

* **高度定制化角色：** 动态配置 AI 昵称与性格特征，模型将严格遵循设定进行拟人化输出。
* **多会话状态隔离：** 支持创建、持久化保存、切换及销毁多个独立对话，上下文互不串扰。
* **流式响应 (Streaming)：** 深度集成大模型流式输出能力，提供低延迟的实时打字机对话体验。
* **本地数据持久化：** 聊天记录与角色元数据均采用 JSON 格式进行本地序列化存储，确保数据不丢失与状态接续。

---

## 项目架构

本项目经历了从单文件脚本到模块化架构的工程化重构：

### Version 3.0 (模块化架构 - 推荐使用)
为提升代码可读性与后期扩展性，V3.0 将核心业务逻辑进行了职责解耦：
* `app.py`：项目主入口，负责 Streamlit 视图层的渲染与用户交互逻辑。
* `config.py`：全局配置中心，集中管理 API 密钥、网络请求参数及 System Prompt 模板。
* `llm.py`：模型驱动层，封装与 DeepSeek API 的网络通信及流式数据流解析。
* `storage.py`：持久化模块，处理本地 JSON 文件的 I/O 操作及会话生命周期管理。

### 历史版本归档
* `AI人物扮演.py` (Version 2.0)：单文件融合版本。包含了视图、通信与存储的所有逻辑，适用于想要快速总览整体流程的开发者。
* `调用.py` (Version 1.0)：早期的基础 API 接口联调测试脚本。

---

## 部署与运行

### 1. 安装环境依赖
确保系统已安装 Python 3.8 或更高版本，随后安装必要的第三方库：

```bash
pip install streamlit openai
```

### 2. 配置环境变量
本项目默认集成 DeepSeek API。运行前需在系统中配置 API Key 环境变量：

**Windows (CMD):**
```cmd
set DEEPSEEK_API_KEY=你的API密钥
```

**Windows (PowerShell):**
```powershell
$env:DEEPSEEK_API_KEY="你的API密钥"
```

**Mac / Linux:**
```bash
export DEEPSEEK_API_KEY="你的API密钥"
```

### 3. 启动服务
在项目根目录下执行以下命令启动应用（推荐使用最新的模块化入口）：

```bash
streamlit run app.py
```
*(注：如需运行历史单文件版本，可执行 `streamlit run AI人物扮演.py`)*

服务启动后，控制台会输出本地访问地址（通常为 `http://localhost:8501`），浏览器会自动打开该页面，即可开始使用。
