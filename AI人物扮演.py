# 导入必要的库
import json
from datetime import datetime
import streamlit as st  # 用于构建Web应用界面
import os  # 用于获取环境变量
from openai import OpenAI  # 用于调用OpenAI API


# 定义AI伴侣的角色设定和对话规则
# %s 是占位符，分别用于插入伴侣昵称和性格特征
Setting=("你叫 %s，现在是用户设定的人物，请完全代入人物角色。"
         "规则:"
         "1.每次尽量只回1条消息，视具体情况可以改变;"
         "2.禁止任何场景或状态描述性文字;"
         "3.匹配用户的语言;"
         "4.回复简短，像微信聊天一样;"
         "5.有需要的话可以用等emoji表情;"
         "6.用符合人物性格的方式对话;"
         "7.回复的内容，要充分体现人物的性格特征"
         "人物性格: %s "
         "你必须严格遵守上述规则来回复用户。")

# 设置Streamlit页面配置
st.set_page_config(
    page_title="这么久没见",  # 页面标题
    page_icon="❤️‍🔥",  # 页面图标
    layout="wide",  # 页面布局为宽屏
    initial_sidebar_state="expanded",  # 初始侧边栏状态为展开
    menu_items={}  # 菜单项（空）
)

# 初始化OpenAI客户端，使用DeepSeek API
client = OpenAI(
    api_key=os.environ.get('DEEPSEEK_API_KEY'),  # 从环境变量获取API密钥
    base_url="https://api.deepseek.com"  # DeepSeek API的基础URL
)



def save_session():
    if st.session_state['current_session']:
        session_data={
            "nick_name":st.session_state['nick_name'],
            "nature":st.session_state['nature'],
            "Messages":st.session_state['Messages'],
            "current_session":st.session_state['current_session'],
        }
        if not os.path.exists("sessions"):
            os.makedirs("sessions")
        with open(f"sessions/{st.session_state['current_session']}.json","w",encoding="utf-8") as f:
            json.dump(session_data,f,ensure_ascii=False,indent=2)

def generate_id():
    return datetime.now().strftime("%Y-%m-%d %H-%M-%S")

#加载所有会话列表信息
def load_sessions():
    session_list=[]
    if os.path.exists("sessions"):
        for file in os.listdir("sessions"):
            if file.endswith(".json"):
                session_list.append(file[:-5])
    session_list.sort(reverse=True)
    return session_list

#加载指定会话
def load_session(session_id):
    try:
        if os.path.exists(f"sessions/{session_id}.json"):
            with open(f"sessions/{session_id}.json", "r", encoding="utf-8") as f:
                session_data = json.load(f)
                st.session_state['nick_name'] = session_data['nick_name']
                st.session_state['nature'] = session_data['nature']
                st.session_state['Messages'] = session_data['Messages']
                st.session_state['current_session'] = session_data['current_session']

    except Exception as e:
        st.error(f"加载会话时出错: {e}")

#删除指定会话
def delete_session(session_id):
    try:
        if os.path.exists(f"sessions/{session_id}.json"):
            os.remove(f"sessions/{session_id}.json")
            if session_id == st.session_state['current_session']:
                st.session_state['Messages'] = []
                st.session_state['current_session'] = generate_id()
        else:
            st.error(f"会话 {session_id} 不存在")
    except Exception as e:
        st.error(f"删除会话时出错: {e}")



# with open(f"sessions/{session_id}.json","w",encoding="utf-8") as f:
#             json.dump(session_data,f,ensure_ascii=False,indent=2)




# 设置页面标题
st.title("AI人物扮演")

# 初始化会话状态变量
# 存储聊天消息历史
if 'Messages' not in st.session_state:
    st.session_state['Messages'] = []

# 存储伴侣昵称，默认值为"小均均"
if 'nick_name' not in st.session_state:
    st.session_state['nick_name'] = "小均均"

# 存储伴侣性格特征，默认值为"活泼开朗阳光的四川姑娘，俏皮，有情感"
if 'nature' not in st.session_state:
    st.session_state['nature'] = "活泼开朗阳光的四川姑娘，俏皮，有情感"

# 存储会话id
if 'current_session' not in st.session_state:
    st.session_state['current_session'] = generate_id()


st.text(f"会话名称:{st.session_state['current_session']}")
# 显示聊天历史
for message in st.session_state['Messages']:
    st.chat_message(message['role']).write(message['content'])

# 左侧侧边栏

st.sidebar.subheader("会话控制面板")
if st.sidebar.button("新建会话",width="stretch",icon="📝"):
    #保存当前会话
    if st.session_state['Messages']:
        save_session()
        st.session_state['Messages'] = []  # 清空聊天历史
        st.session_state['current_session'] = generate_id()  # 更新会话id为新的id
        st.rerun()


st.sidebar.text("会话历史")
session_list=load_sessions()
for session in session_list:
    col1,col2=st.sidebar.columns([4,1])
    with col1:
        if st.button(session,width='stretch',icon="📑",key=f"load_{session}",type="primary" if session == st.session_state['current_session'] else "secondary"):
            # 加载会话数据
            load_session(session)
            st.rerun()
    with col2:
        if st.button("",width="stretch",icon="❌",key=f"delete_{session}"):
            # 删除会话数据
            delete_session(session)
            st.rerun()


#分割线
st.sidebar.divider()


st.sidebar.subheader("人物信息")

# 输入伴侣昵称的文本框
nick_name = st.sidebar.text_input("昵称",placeholder="请输入人物的昵称",value=st.session_state['nick_name'])
if nick_name:
    st.session_state['nick_name'] = nick_name  # 更新会话状态中的昵称

# 输入伴侣性格特征的文本区域
nature = st.sidebar.text_area("性格",placeholder="请输入人物的性格特征",value=st.session_state['nature'])
if nature:
    st.session_state['nature'] = nature  # 更新会话状态中的性格特征

# 聊天输入框
prompt = st.chat_input("请输入你想说的话")
if prompt:
    # 显示用户输入的消息
    st.chat_message("user").write(prompt)
    # 将用户消息添加到聊天历史
    st.session_state['Messages'].append({"role": "user", "content": prompt})
    
    # 调用DeepSeek API获取AI回复
    response = client.chat.completions.create(
        model="deepseek-chat",  # 使用的模型
        messages=[
            # 系统消息，包含角色设定和规则
            {"role": "system", "content":Setting % (st.session_state['nick_name'],st.session_state['nature'])},
            # 聊天历史
            *st.session_state['Messages'],
        ],
        stream=True  # 启用流式输出
    )
    
    # 非流式输出解析（已注释）
    # st.chat_message("assistant").write(response.choices[0].message.content)
    
    # 流式输出解析
    response_messages=st.empty()  # 创建一个空容器用于显示流式输出
    full_response=""  # 存储完整的回复内容
    
    # 遍历API返回的每个 chunk
    for chunk in response:
        if chunk.choices[0].delta.content is not None:
            # 累加获取的内容
            full_response+=chunk.choices[0].delta.content
            # 更新显示的内容
            response_messages.chat_message("assistant").write(full_response)
    
    # 将AI回复添加到聊天历史
    st.session_state['Messages'].append({"role": "assistant", "content": full_response})

    # 保存当前会话
    save_session()
    st.rerun()