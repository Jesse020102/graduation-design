import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

if 'user_id' not in st.session_state or not st.session_state['user_id']:
    st.error("请现在主菜单界面输入你的用户名")
    st.stop()

# 设置页面标题
st.title('查询页面')

# 在侧边栏创建一个下拉选择器，让用户选择查询部分
query_section = st.sidebar.selectbox(
    '选择查询部分',
    ('学习信息查询', '化学物质查询')
)
# 将学习时长字符串转换为秒的函数
def convert_to_seconds(time_str):
    try:
        parts = time_str.split(':')
        hours, minutes = map(int, parts[:2])
        seconds_parts = parts[2].split('.')
        seconds = int(seconds_parts[0])
        milliseconds = int(float('0.' + seconds_parts[1]) * 1000) if len(seconds_parts) > 1 else 0
        total_seconds = hours * 3600 + minutes * 60 + seconds + milliseconds / 1000
        return total_seconds
    except ValueError as e:
        print(f"Error parsing time: {time_str} with error: {e}")
        return None
# 根据用户选择的查询部分显示不同的内容
if query_section == '学习信息查询':
    st.header('学习信息查询')

    # 读取学习信息文件
    study_info_path = 'data/study_information.csv'
    study_data = pd.read_csv(study_info_path)

    # 使用主菜单中输入的用户名
    username = st.session_state['user_id']

    # 展示该用户的学习信息记录
    user_data = study_data[study_data['用户名'] == username].copy()

    if not user_data.empty:
        st.write(f"{username} 的学习信息记录：")
        st.dataframe(user_data)

        # 转换学习时长为秒
        user_data['学习时长秒'] = user_data['学习时长'].apply(convert_to_seconds)

        # 创建条形图数据
        study_duration_sum = user_data.groupby('学习板块')['学习时长秒'].sum()
        study_modules = study_duration_sum.index.tolist()
        total_study_seconds = study_duration_sum.values

        # 将秒转换为小时
        total_study_hours = total_study_seconds / 3600

        # 绘制条形图
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        plt.figure(figsize=(10, 6))
        plt.bar(study_modules, total_study_hours, color='skyblue')
        plt.xlabel('学习板块')
        plt.ylabel('总学习时长（小时）')
        plt.title(f"{username} 的学习时长条形图")
        plt.xticks(rotation=45)
        st.pyplot(plt)
    else:
        st.warning('没有找到该用户的学习信息。')

    # 这里添加学习信息查询的相关代码和逻辑

elif query_section == '化学物质查询':
    st.header('化学物质查询')

    # 读取化学物质数据文件
    chem_data_path = 'data/search_data.csv'
    chem_data = pd.read_csv(chem_data_path)

    # 创建一个文本输入框让用户输入查询条件
    search_query = st.text_input("请输入化学物质的名称或CAS号码进行搜索：",placeholder="请输入要查询的物质，可以是中文名、CAS号码、化学式", key="search")

    # 创建一个确定按钮
    search_button = st.button("搜索")
    # 当用户点击搜索按钮时，执行搜索
    if search_button:
        # 使用正则表达式的方式进行不区分大小写的模糊搜索
        filtered_data = chem_data[chem_data['中文名'].str.contains(search_query, case=False, na=False) |
                                  chem_data['分子式'].str.contains(search_query, case=False, na=False) |
                                  chem_data['CAS登录号'].str.contains(search_query, case=False, na=False)]

        if not filtered_data.empty:
            st.write("搜索结果：")
            # 遍历过滤后的数据并展示每一项内容
            for index, row in filtered_data.iterrows():
                st.subheader(f"{row['中文名']} ({row['CAS登录号']})")
                st.write(f"CAS号码: {row['CAS登录号']}")
                st.write(f"中文名: {row['中文名']}")
                st.write(f"英文名: {row['英文名']}")
                st.write(f"分子式: {row['分子式']}")

                # 构建图片路径
                image_path = f"data/chaxun_image/{row['CAS登录号']}.jpg"
                # 检查图片文件是否存在
                if os.path.isfile(image_path):
                    st.image(image_path, caption=f"{row['中文名']} ({row['CAS登录号']})")
                else:
                    st.warning(f"没有找到 {row['CAS登录号']} 的图片。")

                st.markdown("---")  # 添加分隔线
        else:
            st.warning("没有找到匹配的化学物质。")