import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton,QDesktopWidget
from chemical_learn_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal
import datetime
import os
import pandas as pd

class Chemical_Learn_Pane(QWidget,Ui_Form):

    show_menu_pane_signal = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(Chemical_Learn_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("化学物质学习界面")
        # 时间模块
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timeElapsed = QTime()
        self.current_index = 0  # 当前展示的数据索引
        self.data = pd.read_excel('resources/search_data.xlsx')
        self.update_display()  # 初始化时更新显示内容










    def chemical_learn_back_menu(self):
        print("返回")
        self.show_menu_pane_signal.emit()

    def update_username1(self, name):
        self.username_label.setText(name)  #  self.username_label 是显示用户名的 QLabel

    # def onComboBoxChanged(self, text):
    #     # 更新 QLabel 的文本为 QComboBox 当前选中的内容
    #     self.label.setText(text)
    def onCloseEvent(self, event):
        self.stopTimer()  # 停止计时器
        self.timeElapsed = QTime()  # 重置时间
        self.timeElapsed.start()  # 重新启动时间
        self.time_label.setText("00:00")  # 更新时间显示
        event.accept()  # 接受关闭事件
        print("测试111")
        self.startTimer()  # 重新启动计时器


    def closeEvent(self, event):
        # 停止计时器并获取学习时间
        self.stopTimer()
        elapsed_time = self.timeElapsed.elapsed()
        study_duration = self.time_label.text()

        # 获取学习板块
        study_module = self.study_label.text()

        # 获取用户名
        username = self.username_label.text()

        # 获取当前日期和时间
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 记录学习信息到文件
        with open("resources/learning_log.csv", "a", encoding="utf-8") as log_file:
            # 如果文件是空的，写入标题行
            if log_file.tell() == 0:
                log_file.write("学习日期时间,用户名,学习时长,学习板块\n")

            # 写入数据行
            log_file.write(f"{current_datetime},{username},{study_duration},{study_module}\n")


        # 调用父类的 closeEvent 方法
        super(Chemical_Learn_Pane, self).closeEvent(event)

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

    def update_display(self):
        # 确保当前索引有效
        if 0 <= self.current_index < len(self.data):
            # 获取当前索引的数据
            current_data = self.data.iloc[self.current_index]
            # 更新文本框内容
            self.textBrowser.setText(current_data['CAS登录号'])
            self.textBrowser_2.setText(current_data['中文名'])
            self.textBrowser_3.setText(current_data['分子式'])
            self.textBrowser_4.setText(current_data['英文名'])
            # 更新图片
            image_filename = f"resources/chaxun_image/{current_data['CAS登录号']}.jpg"
            self.load_image(image_filename)
        else:
            QMessageBox.information(self, "提示", "索引超出范围。")
    def load_image(self, image_filename):
        pixmap = QPixmap(image_filename)
        if not pixmap.isNull():
            self.picture_label.setPixmap(pixmap)
            self.picture_label.setScaledContents(True)  # 如果需要图片自适应 QLabel 大小
        else:
            QMessageBox.information(self, "错误", "无法加载图片。")

    def chaxun_back_menu(self):
        print("返回")
        self.show_menu_pane_signal.emit()

    def last_page(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.update_display()

    def next_page(self):
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self.update_display()

    def enter(self):
        page_number= self.lineEdit.text()
        try:
            page = int(self.lineEdit.text())
            if 0 <= page < len(self.data):
                self.current_index = page
                self.update_display()
            else:
                QMessageBox.information(self, "提示", "页码超出范围。")
        except:
            QMessageBox.information(self, "提示", "请输入数字。")































if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = Chemical_Learn_Pane()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)