import os
import json
from datetime import datetime
import streamlit as st
from config import SESSION_DIR

def init_session_dir():
    """确保存储会话的目录存在"""
    if not os.path.exists(SESSION_DIR):
        os.makedirs(SESSION_DIR)

def generate_id():
    """生成基于时间的会话ID"""
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

def save_session():
    """保存当前会话到JSON文件"""
    init_session_dir()
    if st.session_state.get('current_session'):
        session_data = {
            "nick_name": st.session_state.get('nick_name'),
            "nature": st.session_state.get('nature'),
            "Messages": st.session_state.get('Messages', []),
            "current_session": st.session_state.get('current_session'),
        }
        file_path = os.path.join(SESSION_DIR, f"{st.session_state['current_session']}.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(session_data, f, ensure_ascii=False, indent=2)

def load_sessions():
    """读取所有历史会话列表"""
    init_session_dir()
    session_list = []
    for file in os.listdir(SESSION_DIR):
        if file.endswith(".json"):
            session_list.append(file[:-5])
    session_list.sort(reverse=True)
    return session_list

def load_session(session_id):
    """加载指定的历史会话"""
    file_path = os.path.join(SESSION_DIR, f"{session_id}.json")
    try:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                session_data = json.load(f)
                # 使用 .get 赋予默认值，防止旧文件缺字段报错
                st.session_state['nick_name'] = session_data.get('nick_name', '小均均')
                st.session_state['nature'] = session_data.get('nature', '活泼开朗阳光的四川姑娘，俏皮，有情感')
                st.session_state['Messages'] = session_data.get('Messages', [])
                st.session_state['current_session'] = session_data.get('current_session', session_id)
    except Exception as e:
        st.error(f"加载会话时出错: {e}")

def delete_session(session_id):
    """删除指定的历史会话"""
    file_path = os.path.join(SESSION_DIR, f"{session_id}.json")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            # 如果删除的是当前正在看的会话，则清空屏幕并新建一个
            if session_id == st.session_state.get('current_session'):
                st.session_state['Messages'] = []
                st.session_state['current_session'] = generate_id()
        else:
            st.error(f"会话 {session_id} 不存在")
    except Exception as e:
        st.error(f"删除会话时出错: {e}")