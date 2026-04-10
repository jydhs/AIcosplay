import streamlit as st
from storage import generate_id, save_session, load_sessions, load_session, delete_session
from llm import get_chat_response_stream

# 1. 页面配置 (必须放在最前面)
st.set_page_config(
    page_title="这么久没见",
    page_icon="❤️‍🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 2. 初始化全局状态
def init_state():
    if 'Messages' not in st.session_state:
        st.session_state['Messages'] = []
    if 'nick_name' not in st.session_state:
        st.session_state['nick_name'] = "小均均"
    if 'nature' not in st.session_state:
        st.session_state['nature'] = "活泼开朗阳光的四川姑娘，俏皮，有情感"
    if 'current_session' not in st.session_state:
        st.session_state['current_session'] = generate_id()


# 3. 渲染侧边栏
def render_sidebar():
    st.sidebar.subheader("会话控制面板")

    # 新建会话按钮
    if st.sidebar.button("新建会话", width="stretch", icon="📝"):
        if st.session_state['Messages']:
            save_session()
        st.session_state['Messages'] = []
        st.session_state['current_session'] = generate_id()
        st.rerun()

    # 历史会话列表
    st.sidebar.text("会话历史")
    session_list = load_sessions()
    for session in session_list:
        col1, col2 = st.sidebar.columns([4, 1])
        with col1:
            is_active = (session == st.session_state['current_session'])
            if st.button(session, width='stretch', icon="📑", key=f"load_{session}",
                         type="primary" if is_active else "secondary"):
                load_session(session)
                st.rerun()
        with col2:
            if st.button("", width="stretch", icon="❌", key=f"delete_{session}"):
                delete_session(session)
                st.rerun()

    st.sidebar.divider()

    # 人物信息设置
    st.sidebar.subheader("人物信息")
    new_nick_name = st.sidebar.text_input("昵称", placeholder="请输入人物的昵称", value=st.session_state['nick_name'])
    if new_nick_name != st.session_state['nick_name']:
        st.session_state['nick_name'] = new_nick_name

    new_nature = st.sidebar.text_area("性格", placeholder="请输入人物的性格特征", value=st.session_state['nature'])
    if new_nature != st.session_state['nature']:
        st.session_state['nature'] = new_nature


# 4. 渲染主聊天区
def render_main_chat():
    st.title("AI人物扮演")
    st.text(f"会话名称:{st.session_state['current_session']}")

    # 回显历史消息
    for message in st.session_state['Messages']:
        st.chat_message(message['role']).write(message['content'])

    # 处理新的用户输入
    prompt = st.chat_input("请输入你想说的话")
    if prompt:
        st.chat_message("user").write(prompt)
        st.session_state['Messages'].append({"role": "user", "content": prompt})

        # 请求 LLM 接口
        response_stream = get_chat_response_stream(
            st.session_state['Messages'],
            st.session_state['nick_name'],
            st.session_state['nature']
        )

        if response_stream:
            response_container = st.empty()
            full_response = ""

            # 流式逐字显示
            for chunk in response_stream:
                if chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    response_container.chat_message("assistant").write(full_response)

            # 保存到记录并持久化
            st.session_state['Messages'].append({"role": "assistant", "content": full_response})
            save_session()
            # 流式输出完后建议rerun一次，确保状态彻底同步(非必须，但体验更稳定)
            st.rerun()


# 启动入口
if __name__ == "__main__":
    init_state()
    render_sidebar()
    render_main_chat()