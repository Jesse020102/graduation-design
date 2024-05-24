# -*- coding: utf-8 -*-
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from kaoshi_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal
import quiz_list
import random
import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# 设置matplotlib的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

# 设置matplotlib的字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
class Kaoshi_Pane(QWidget,Ui_Form):

    show_menu_pane_signal=pyqtSignal()


    def __init__(self, parent=None, *args, **kwargs):
        super(Kaoshi_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("考试系统")

        self.optionlist = [self.radioButton_A, self.radioButton_B, self.radioButton_C, self.radioButton_D]
        self.quiz_num = []  # 创建抽取的题目号的空列表 0~99
        self.quiz_box = []  # 创建用于存储抽取的题目的空列表

        self.count = 0  # 记录题目数量

        self.setupQuizCountComboBox()  # 设置题目数量下拉菜单
        self.setuphardCountComboBox()  # 设置难度系数下拉菜单
        self.Extract_Quiz()
        self.Set_Text()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timeElapsed = QTime()
        self.current_index = 0  # 当前展示的数据索引
        # self.set_time_lable()
        # 按钮信号
        self.option = None  # 初始化选项为空
        self.radioButton_A.toggled.connect(lambda: self.setOption(1))
        self.radioButton_B.toggled.connect(lambda: self.setOption(2))
        self.radioButton_C.toggled.connect(lambda: self.setOption(3))
        self.radioButton_D.toggled.connect(lambda: self.setOption(4))
        # 安装关闭事件处理器
        self.closeEvent = self.onCloseEvent
        self.user_answers = [None] * len(self.quiz_box)

        # 得分计算实时

        self.score = 0  # 初始化分数为0
        self.update_score_label()  # 更新分数显示

    def update_score_label(self):
        self.score_label.setText(str(self.score))  # 分数转换为字符串显示
    def reset_score(self):
        self.score = 0
        self.update_score_label()



    def onCloseEvent(self, event):
        self.stopTimer()  # 停止计时器
        self.timeElapsed = QTime()  # 重置时间
        self.timeElapsed.start()  # 重新启动时间
        self.time_label.setText("00:00")  # 更新时间显示
        event.accept()  # 接受关闭事件
        print("测试111")
        self.startTimer()  # 重新启动计时器

    def closeEvent(self, event):
        self.stopTimer()  # 停止计时器
        event.accept()  # 接受关闭事件
    def kaoshi_back_menu(self):
        print("返回")

        self.show_menu_pane_signal.emit()

    def showEvent(self, event):
        super().showEvent(event)
        self.startTimer()  # 窗口显示时开始计时

    def hideEvent(self, event):
        super().hideEvent(event)
        self.stopTimer()  # 窗口隐藏时停止计时

    def startTimer(self):

        self.timeElapsed.start()
        self.timer.start(1000)  # update every second

    def stopTimer(self):
        self.timer.stop()
        print("停止计时")
        print("停留时间：", self.timeElapsed.elapsed())

    def updateTime(self):
        elapsed_ms = self.timeElapsed.elapsed()
        elapsed_time = QTime(0, 0).addMSecs(elapsed_ms)  # 从0点开始加上经过的毫秒数
        self.time_label.setText(elapsed_time.toString('mm:ss'))

    def kaoshi_back_menu(self):
        print("返回")
        self.startTimer()
        self.show_menu_pane_signal.emit()

    def Extract_Quiz(self):
        print("Extracting new quiz based on difficulty...")
        self.quiz_num.clear()
        self.quiz_box.clear()
        # 获取用户选择的难度系数
        selected_difficulty = self.selectedDifficulty
        # 筛选出符合难度系数的题目索引
        filtered_indexes = [index for index, difficulty in enumerate(quiz_list.hard_list) if
                            difficulty == selected_difficulty]
        # 检查筛选后的题目数量是否满足要求
        if len(filtered_indexes) < self.currentQuizCount:
            # 处理题目数量不足的情况
            QMessageBox.warning(self, "警告", "根据所选难度系数，题目数量不足。请减少题目数量或选择其他难度系数。")
            return  # 退出方法，不继续抽取题目

        # 随机选择题目索引
        selected_indexes = random.sample(filtered_indexes, self.currentQuizCount)

        # 根据索引抽取题目
        for index in selected_indexes:
            question_type = quiz_list.type_list[index]
            self.quiz_box.append((quiz_list.str_test[index], question_type))
            self.quiz_num.append(index)  # 确保同时更新 self.quiz_num 列表

        # 重置用户答案列表的大小
        self.user_answers = [None] * len(self.quiz_box)

        # 显示第一个题目
        self.count = 0
        self.Set_Text()

    def setOption(self, option):
        if self.sender().isChecked():
            print(f"Question {self.count + 1} option selected: {option}")
            if self.count < len(self.user_answers):  # 确保索引有效
                self.user_answers[self.count] = option

    def last_question(self):
        if self.count > 0:
            self.save_current_answer()
            self.count -= 1
            self.updateRadioButtonState()  # 更新单选按钮的状态
            self.Set_Text()
        else:
            QMessageBox.about(self, "提示", "这已经是第一题了！")


    def next_question(self):
        if self.count < len(self.quiz_box) - 1:  # 确保不超过题目总数
            self.save_current_answer()

            self.count += 1
            self.updateRadioButtonState()  # 更新单选按钮的状态
            self.Set_Text()
        else:
            QMessageBox.about(self, "提示", "这已经是最后一题了！")

    def save_current_answer(self):
        current_question, question_type = self.quiz_box[self.count]
        if question_type == 1:
            # 单选题，已经保存在 user_answers 中
            pass
        elif question_type == 2:
            # 填空题，保存输入框的内容
            self.user_answers[self.count] = self.lineEdit.text()
        elif question_type == 3:
            # 填空题，保存输入框的内容
            self.user_answers[self.count] = self.lineEdit_2.text()
    def updateRadioButtonState(self):
        current_question, question_type = self.quiz_box[self.count]
        user_answer = self.user_answers[self.count]
        if question_type == 1:
            # 单选题
            if user_answer is not None and isinstance(user_answer, int):
                self.optionlist[user_answer - 1].setChecked(True)
        elif question_type == 2:
            # 填空题
            # 对于填空题，不需要更新单选按钮的状态
            pass

    def Set_Text(self):           # 显示抽取的题目
        current_question, question_type = self.quiz_box[self.count]

        print(f"当前题目: {current_question}")
        print(f"题目类型: {question_type}")

        if question_type == 1:
            # 显示单选题布局
            self.stackedWidget.setCurrentIndex(0)
            # 确保 current_question 包含足够的元素
            if len(current_question) >= 5:
                self.textBrowser.setText(str("{}、".format(self.count + 1)) + current_question[0])
                self.radioButton_A.setText(current_question[1])
                self.radioButton_B.setText(current_question[2])
                self.radioButton_C.setText(current_question[3])
                self.radioButton_D.setText(current_question[4])
            else:
                print("Error: 单选题数据格式不正确")
                print(f"题目索引: {self.count}, 题目内容: {current_question}")
            # 更新单选题内容
        elif question_type == 2:
            # 显示填空题布局
            self.stackedWidget.setCurrentIndex(2)
            # 设置填空题内容
            if len(current_question) >= 1:
                self.textBrowser_2.setText(str("{}、".format(self.count + 1)) + current_question)
                print(current_question[0])
                user_answer = self.user_answers[self.count]
                if user_answer is not None:
                    self.lineEdit.setText(user_answer)
                else:
                    self.lineEdit.clear()
        elif question_type == 3:
        # 显示带图片的填空题布局
            self.stackedWidget.setCurrentIndex(1)
            if len(current_question) >= 1:
                self.chemical_textbrowser.setText(str("{}、".format(self.count + 1)) + current_question)

                # 提取第8到第14个字符作为图片的一部分路径
                image_code = current_question[7:14]
                image_filename = f"resources\chaxun_image\{image_code}.jpg"
                self.load_image(image_filename)

                print(current_question[0])
                user_answer = self.user_answers[self.count]
                if user_answer is not None:
                    self.lineEdit_2.setText(user_answer)
                else:
                    self.lineEdit.clear()
            else:
                print("Error: 填空题数据格式不正确")

    def load_image(self, image_filename):
        pixmap = QPixmap(image_filename)
        if not pixmap.isNull():
            self.chemical_picture_label.setPixmap(pixmap)
            self.chemical_picture_label.setScaledContents(True)  # 如果需要图片自适应 QLabel 大小
        # else:
        #     QMessageBox.information(self, "错误", "无法加载图片。")

    def showMultipleChoiceLayout(self):
        self.addWidget(self.radioButton_A)
        self.addWidget(self.radioButton_B)
        self.addWidget(self.radioButton_C)
        self.addWidget(self.radioButton_D)
        self.removeWidget(self.textBrowser_2)
        self.removeWidget(self.lineEdit)


    def set_time_lable(self):
        self.startTimer()

    def setupQuizCountComboBox(self):
        self.quizCountComboBox.addItems(["10", "20", "50","100"])
        self.quizCountComboBox.currentIndexChanged.connect(self.onQuizCountChanged)
        self.currentQuizCount = 10  # 默认题目数量

    def setuphardCountComboBox(self):
        self.hardCountComboBox.addItems(["1", "2", "3", "4", "5"])
        self.hardCountComboBox.currentIndexChanged.connect(self.onHardCountChanged)
        self.selectedDifficulty = 1  # 默认难度系数
    def onQuizCountChanged(self, index):
        # 根据用户选择设置题目数量
        self.currentQuizCount = int(self.quizCountComboBox.currentText())
        self.resetQuiz()  # 重置题目和分数

    def onHardCountChanged(self, index):
        # 根据用户选择设置难度系数
        self.selectedDifficulty = int(self.hardCountComboBox.currentText())
        self.resetQuiz()  # 重置题目和分数
    def resetQuiz(self):
        self.reset_score()  # 重置分数
        self.Extract_Quiz()  # 重新提取题

    def hand_in(self):
        correct_answers = 0
        # 确保在评分前保存当前题目的答案
        self.save_current_answer()
        for i in range(len(self.quiz_box)):
            current_question, question_type = self.quiz_box[i]
            user_answer = self.user_answers[i]
            # 从 self.quiz_num 获取原始题库中的索引
            original_index = self.quiz_num[i]
            correct_answer = quiz_list.answer[original_index]  # 使用原始索引从答案列表中获取正确答案
            print(f"题目 {i + 1}: 用户答案={user_answer}, 正确答案={correct_answer}")  # 调试信息

            if question_type == 1 and isinstance(user_answer, int) and isinstance(correct_answer, int):
                # 对于单选题，比较选项是否正确
                if user_answer == correct_answer:
                    correct_answers += 1
            elif question_type == 2 and isinstance(user_answer, str) and isinstance(correct_answer, str):
                # 对于填空题，比较答案是否正确
                if user_answer.strip() == correct_answer.strip():
                    correct_answers += 1
            elif question_type == 3 and isinstance(user_answer, str) and isinstance(correct_answer, str):
                if user_answer.strip() == correct_answer.strip():
                    correct_answers += 1
        # 计算分数和正确率
        total_questions = len(self.quiz_box)
        score_per_question = 100 / total_questions
        score = correct_answers * score_per_question
        correct_rate = correct_answers / total_questions if total_questions > 0 else 0

        # 显示分数和正确率的对话框
        if score>=60:
            QMessageBox.information(self, "成绩单", f"您的分数是：{score}\n正确率：{correct_rate * 100}%,很棒哦！要继续再接再励！")
        else:
            QMessageBox.information(self, "成绩单", f"您的分数是：{score}\n正确率：{correct_rate * 100}%,还得继续加油哦！")

        # 绘制饼图
        self.show_pie_chart(correct_answers, total_questions - correct_answers)

    def get_user_option(self, question_index):
        # self.optionlist中的radiobuttons顺序与答案的顺序一致
        for i, radio_button in enumerate(self.optionlist):
            if radio_button.isChecked():
                # 返回用户选择的选项编号（1-4）
                return i + 1
        return None  # 如果没有选项被选中，返回None

    def extract_quiz_by_difficulty(selected_difficulty, count):
        # 筛选出符合难度系数的题目索引
        filtered_indexes = [index for index, difficulty in enumerate(quiz_list.hard_list) if difficulty == selected_difficulty]

        # 随机选择题目索引
        selected_indexes = random.sample(filtered_indexes, min(count, len(filtered_indexes)))

        # 根据索引抽取题目
        selected_quizzes = [quiz_list[index] for index in selected_indexes]

        return selected_quizzes
    def show_pie_chart(self, correct_answers, incorrect_answers):
        import matplotlib.pyplot as plt

        # 数据准备
        labels = '正确', '错误'
        sizes = [correct_answers, incorrect_answers]
        colors = ['lightgreen', 'lightcoral']
        explode = (0.1, 0)  # 突出显示正确答案的切片

        # 绘制饼图
        plt.figure(figsize=(8, 6))  # 设置图表大小
        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)

        # 添加标题
        plt.title('考试成绩分布')

        # 确保饼图为圆形
        plt.axis('equal')

        # 显示图表
        plt.show()

if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        kaoshi_WD = Kaoshi_Pane()
        kaoshi_WD.show()
        sys.exit(app.exec_())
    except Exception as e:
        import traceback
        print("Exception:", e)
        traceback.print_exc()