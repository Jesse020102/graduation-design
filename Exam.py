import streamlit as st
import random
import sys
import os
import time
sys.path.append(os.path.abspath("C:/Users/Administrator/PycharmProjects/biyesheji/streamlit"))
import quiz_list
import matplotlib.pyplot as plt
# 初始化Session State


def extract_questions(difficulty, count):
    filtered_indexes = [index for index, hard in enumerate(quiz_list.hard_list) if hard == difficulty]
    selected_indexes = random.sample(filtered_indexes, min(count, len(filtered_indexes)))
    extracted_questions = []
    for i in selected_indexes:
        question_data = quiz_list.str_test[i]
        correct_answer = quiz_list.answer[i]
        question_type = quiz_list.type_list[i]
        # 根据题目类型添加不同的处理逻辑
        if question_type == 1:  # 选择题
            extracted_questions.append((question_data, correct_answer, question_type))
        elif question_type == 2:  # 填空题
            extracted_questions.append((question_data, correct_answer, question_type))
        elif question_type == 3:  # 带图片的填空题
            extracted_questions.append((question_data, correct_answer, question_type))
    return extracted_questions

# 定义重新抽取题目并更新 session state 的函数
def update_questions():
    # 抽取新的题目
    new_questions = extract_questions(st.session_state['difficulty'], st.session_state['quiz_count'])
    # 更新 session state
    st.session_state['questions'] = new_questions
    st.session_state['user_answers'] = {i: None for i in range(len(new_questions))}
# 确保用户已经在主界面输入了用户 ID
if 'user_id' not in st.session_state or not st.session_state['user_id']:
    st.error("请先在主界面输入您的用户ID。")
    st.stop()
else:
    user_id = st.session_state['user_id']  # 使用已经输入的用户 ID

if 'initialized' not in st.session_state:
    st.session_state['initialized'] = True
    st.session_state['user_answers'] = {}
    st.session_state['questions'] = []
    st.session_state['quiz_count'] = 10  # 默认题目数量
    st.session_state['difficulty'] = 1   # 默认难度

# 初始化 session state 中的计时器开始时间
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()




# 难度系数和题目数量选择栏，始终显示在侧边栏
quiz_count = st.sidebar.selectbox("选择题目数量", [10, 20, 50, 100], key="quiz_count", on_change=update_questions)
difficulty = st.sidebar.selectbox("选择难度", [1, 2, 3, 4, 5], key="difficulty", on_change=update_questions)




# 如果 session state 中的题目列表为空，或者是首次运行，则抽取题目
if not st.session_state['questions']:
    update_questions()

# 使用表单来防止页面刷新
with st.form(key="question_form"):

    for i, (question_data, correct_answer, question_type) in enumerate(st.session_state.questions):
        if question_type == 1:
            # 选择题
            question, *options = question_data  # 解包问题和选项
            st.write(f"问题 {i+1}: {question}")
            key = f"question_{i}"
            selected_option = st.radio("", options, key=key,index=0)
            if selected_option:
                st.session_state.user_answers[i] = options.index(selected_option) + 1
        elif question_type == 2:
            # 填空题
            question = question_data  # 填空题只有问题文本
            st.write(f"问题 {i+1}: {question}")
            key = f"question_{i}"
            user_input = st.text_input("", key=key)
            if user_input:
                st.session_state.user_answers[i] = user_input.strip()
        elif question_type == 3:
            # 带图片的填空题
            question = question_data  # 假设带图片的填空题也只有问题文本
            st.write(f"问题 {i+1}: {question}")
            key = f"question_{i}"
            user_input = st.text_input("",placeholder="请输入答案", key=key)
            image_code = question[7:14]  # 获取题目的第8到第14个字符
            image_path = f"data/chaxun_image/{image_code}.jpg"  # 构建图片路径
            st.image(image_path, caption="问题图片", use_column_width=True)
            if user_input:
                st.session_state.user_answers[i] = user_input.strip()

    submitted = st.form_submit_button('提交答案')
    if submitted:
        # ...之前的代码...

        # 初始化题型的正确数量和总数量
        correct_by_type = {1: 0, 2: 0, 3: 0}
        total_by_type = {1: 0, 2: 0, 3: 0}

        # 遍历用户答案和问题，进行判分
        for i, (user_answer, (_, correct_answer, question_type)) in enumerate(
                zip(st.session_state['user_answers'].values(), st.session_state['questions'])):
            # 更新题型的总题目数量
            total_by_type[question_type] += 1

            # 检查答案是否正确
            if question_type == 1:
                # 选择题的答案是选项的索引
                if user_answer == correct_answer:
                    correct_by_type[question_type] += 1
            else:
                # 填空题和带图片的填空题的答案是字符串
                # 在比较之前确保 user_answer 不是 None
                user_answer = '' if user_answer is None else user_answer.strip().lower()
                correct_answer = correct_answer.strip().lower()
                if user_answer == correct_answer:
                    correct_by_type[question_type] += 1

        # 计算每种题型的正确率
        accuracy_by_type = {q_type: (correct_by_type[q_type] / total_by_type[q_type]) * 100
                            for q_type in total_by_type if total_by_type[q_type] > 0}

        # 创建对比图
        fig, ax1 = plt.subplots()

        # 绘制每种题型的正确率
        bars = ax1.bar(accuracy_by_type.keys(), accuracy_by_type.values(), color='lightblue', label='正确率')

        # 在每个条形上方添加总题数注释
        for bar, total in zip(bars, total_by_type.values()):
            yval = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'总题数: {total}', ha='center', va='bottom')

        # 设置图表标题和轴标签
        ax1.set_xlabel('题型')
        ax1.set_ylabel('正确率 (%)')
        ax1.set_ylim(0, 100)  # 正确率范围从0到100
        ax1.set_xticks(list(accuracy_by_type.keys()))  # 设置x轴刻度
        ax1.set_xticklabels(['选择题', '填空题', '化学计算'])  # 设置x轴刻度标签

        # 显示图例
        ax1.legend()

        # 在Streamlit中展示图表
        st.pyplot(fig)