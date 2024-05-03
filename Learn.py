import sys
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime
if 'user_id' not in st.session_state or not st.session_state['user_id']:
    st.error("请现在主菜单界面输入你的用户名")
    st.stop()


# 定义每个学习部分的子主题或课程
video_topics = {
    '化学实验 一': 'resources/videos/gzsy_1.mp4',
    '化学实验 二': 'resources/videos/gzsy_2.mp4',
    '化学实验 三': 'resources/videos/gzsy_3.mp4',
    '化学实验 四': 'resources/videos/gzsy_4.mp4',
    '化学实验 五': 'resources/videos/gzsy_5.mp4',
    '化学实验 六': 'resources/videos/gzsy_6.mp4',
    '化学实验 七': 'resources/videos/gzsy_7.mp4',
    '化学实验 八': 'resources/videos/gzsy_8.mp4',
    '化学实验 九': 'resources/videos/gzsy_9.mp4',
    '化学实验 十': 'resources/videos/gzsy_10.mp4',
    '化学实验 十一': 'resources/videos/gzsy_11.mp4',
    '化学实验 十二': 'resources/videos/gzsy_12.mp4',
    '化学实验 十三': 'resources/videos/gzsy_13.mp4',
    '我们需要化学 第一集': 'resources/videos/kepu_1.mp4',
    '我们需要化学 第二集': 'resources/videos/kepu_2.mp4',
    '我们需要化学 第三集': 'resources/videos/kepu_3.mp4',
    '我们需要化学 第四集': 'resources/videos/kepu_4.mp4',
    '我们需要化学 第五集': 'resources/videos/kepu_5.mp4',
    '我们需要化学 第六集': 'resources/videos/kepu_6.mp4',
}
# 读取JSON文件
with open('data/learning_topics.json', 'r', encoding='utf-8') as json_file:
    image_topics = json.load(json_file)


# 在侧边栏创建一个下拉选择器
learning_section = st.sidebar.selectbox(
    '选择学习部分',
    ('视频学习', '图文学习', '化学物质学习')
)
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = None

if st.sidebar.button("开始学习"):
    st.session_state['start_time'] = datetime.now().replace(microsecond=0)
    formatted_start_time = st.session_state['start_time'].strftime('%Y-%m-%d %H:%M:%S')
    st.sidebar.success(f"学习开始时间: {formatted_start_time}")

if st.sidebar.button("结束学习"):
    if st.session_state['start_time'] is not None:
        # 获取当前时间并去除毫秒部分
        end_time = datetime.now().replace(microsecond=0)
        study_duration = end_time - st.session_state['start_time']
        # 获取总秒数并转换为整数
        total_seconds = int(study_duration.total_seconds())
        # 格式化时长为 HH:MM:SS
        formatted_duration = f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}:{total_seconds % 60:02d}"

        st.sidebar.success(f"学习结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        st.sidebar.success(f"学习时长: {formatted_duration}")

        # 记录学习信息到文件
        study_info = {
            '学习日期时间': st.session_state['start_time'].strftime("%Y-%m-%d %H:%M:%S"),
            '用户名': st.session_state['user_id'],
            '学习时长': formatted_duration,  # 使用格式化后的时长
            '学习板块': learning_section
        }
        study_log_path = 'data/study_information.csv'
        # 检查文件是否存在，如果不存在则写入标题行
        if not os.path.isfile(study_log_path):
            with open(study_log_path, 'w', encoding='utf-8') as file:
                file.write('学习日期时间,用户名,学习时长,学习板块\n')

        # 写入数据
        with open(study_log_path, 'a', encoding='utf-8') as file:
            file.write(
                f"{study_info['学习日期时间']},{study_info['用户名']},{study_info['学习时长']},{study_info['学习板块']}\n")
        st.sidebar.success("学习信息已记录")
    else:
        st.sidebar.error("请先点击开始学习")
# 根据选择的学习部分，在侧边栏显示另一个选择器
if learning_section == '视频学习':
    topic = st.sidebar.selectbox('选择视频主题', list(video_topics.keys()))
    st.header(f'视频学习 - {topic}')
    # 显示选定视频主题的内容
    video_path = video_topics[topic]
    st.video(video_path)
elif learning_section == '图文学习':
    topic = st.sidebar.selectbox('选择内容板块', list(image_topics.keys()))
    selected_topic = image_topics[topic]  # 获取选择的板块内容
    st.header(f'图文学习 - {selected_topic["title"]}')
    # 遍历板块内容，显示文字和图片
    for item in selected_topic['contents']:
        if item.endswith(('.png', '.jpg', '.jpeg', '.gif')):  # 假设图片文件以这些扩展名结尾
            st.image(item)  # 显示图片
        else:
            st.write(item)  # 显示文字
elif learning_section == '化学物质学习':

    st.header(f'化学物质学习')
    # 读取CSV文件
    csv_path = 'C:/Users/Administrator/PycharmProjects/biyesheji/streamlit/data/search_data.csv'
    data = pd.read_csv(csv_path)

    if 'selected_index' not in st.session_state:
        st.session_state.selected_index = 0  # 初始化selected_index

    selected_index = st.session_state.selected_index

    # 使用st.session_state.selected_index来获取和展示数据
    selected_data = data.iloc[st.session_state.selected_index]

    # 展示选中的化学物质的信息
    st.write(f"CAS登录号: {selected_data['CAS登录号']}")
    st.write(f"中文名: {selected_data['中文名']}")
    st.write(f"分子式: {selected_data['分子式']}")
    st.write(f"英文名: {selected_data['英文名']}")

    # 展示图片
    image_filename = f"data/chaxun_image/{selected_data['CAS登录号']}.jpg"
    st.image(image_filename, caption=f"{selected_data['中文名']} ({selected_data['CAS登录号']})")
    # 然后在上一页和下一页按钮的处理中更新st.session_state.selected_index
    if st.button('上一页') and selected_index > 0:
        st.session_state.selected_index -= 1

    if st.button('下一页') and selected_index < len(data) - 1:
        st.session_state.selected_index += 1
    # 获取用户输入的页码
    page_number = st.number_input('跳转到页码', min_value=0, max_value=len(data)-1, step=1)

    # 如果用户点击了跳转按钮
    if st.button('跳转'):
        # 更新Session State中的selected_index为用户输入的页码
        st.session_state.selected_index = page_number
        # 每次按钮被点击后，重新运行页面以更新显示内容
        st.experimental_rerun()

