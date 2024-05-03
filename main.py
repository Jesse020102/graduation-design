import streamlit as st

# 设置页面配置
st.set_page_config(page_title="化学化工知识学习及水平考试系统", layout="wide")

# 可选：展示一些欢迎信息或应用介绍
st.title("欢迎来到化学化工知识学习及水平考试系统")
st.write("""
制作人：梁桀熙（celjx@mail.scut.edu.cn)，指导老师：方利国(lgfang@scut.edu.cn)

华南理工大学毕业设计

本软件参考了维基百科，爱化学，bilibili视频，百度文库，必应图库，知乎，github等网络资料

如有侵权请联系作者删除

本软件包含了三个主要板块，知识学习板块，考试板块和搜索板块

请从左侧导航栏进入页面

本软件遵循Apache协议

""")
# 用户ID输入
if 'user_id' not in st.session_state or not st.session_state['user_id']:
    user_input = st.text_input("请输入您的用户ID以继续：", key="user_input")
    if st.button('确定'):
        if user_input:
            st.session_state['user_id'] = user_input
            st.success(f"欢迎，用户 {user_input}!")
            st.stop()  # 停止执行，显示欢迎信息
        else:
            st.error("用户ID不能为空，请输入您的用户ID。")
else:
    st.success(f"欢迎回来，用户 {st.session_state['user_id']}!")
