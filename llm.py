from openai import OpenAI
import streamlit as st
from config import API_KEY, BASE_URL, MODEL_NAME, SYSTEM_PROMPT_TEMPLATE

# 初始化客户端
client = OpenAI(
    api_key=API_KEY,
    base_url=BASE_URL
)


def get_chat_response_stream(messages, nick_name, nature):
    """构建Prompt并调用API返回流式结果"""
    # 组合System Prompt
    system_message = {
        "role": "system",
        "content": SYSTEM_PROMPT_TEMPLATE % (nick_name, nature)
    }

    # 拼接完整消息上下文
    full_messages = [system_message] + messages

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=full_messages,
            stream=True
        )
        return response
    except Exception as e:
        st.error(f"调用模型时发生错误: {e}")
        return None