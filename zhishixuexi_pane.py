import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton,QDesktopWidget
from zhishixuexi_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal
import zhishi_list
import datetime
from PyQt5.QAxContainer import QAxWidget
import os
class Zhishixuexi_Pane(QWidget,Ui_Form):

    show_menu_pane_signal = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(Zhishixuexi_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.axWidget = QAxWidget(self)
        self.horizontalLayout.addWidget(self.axWidget)
        # 连接 QComboBox 的 currentTextChanged 信号到槽函数
        # self.comboBox.currentTextChanged.connect(self.onComboBoxChanged)
        self.setWindowTitle("知识学习")
        # 时间模块
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timeElapsed = QTime()
        self.add_zs()  # 添加实验并显示
        self.comboBox.currentTextChanged.connect(self.choose_zs)


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
        study_module = self.comboBox.currentText()

        # 获取用户名
        username = self.username_label.text()

        # 获取当前日期和时间
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        # 记录学习信息到文件
        with open("resources/learning_log.csv", "a", encoding="utf-8") as log_file:
            # 如果文件是空的，写入标题行
            if study_module == "请选择学习内容(如果页面过大或过小，可通过‘ctrl + 鼠标滚轮’调整大小)":
                pass
            else:
                if log_file.tell() == 0:
                    log_file.write("学习日期时间,用户名,学习时长,学习板块\n")

                # 写入数据行
                log_file.write(f"{current_datetime},{username},{study_duration},{study_module}\n")

        # 如果 axWidget 直接添加到 QWidget 而没有使用布局
        if self.axWidget is not None:
            # self.axWidget.close()
            # self.axWidget.deleteLater()  # 使用 deleteLater 安全删除对象
            self.horizontalLayout.removeWidget(self.axWidget)
        # 如果 axWidget 添加到了布局中
        # # 检查是否有布局，如果有，从布局中移除 axWidget
        # if self.layout() is not None:
        #     self.layout().removeWidget(self.axWidget)
        #     self.axWidget.deleteLater()  # 使用 deleteLater 安全删除对象

        # 调用父类的 closeEvent 方法
        super(Zhishixuexi_Pane, self).closeEvent(event)

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






    def zhishixuexi_back_menu(self):
        print("返回")
        self.show_menu_pane_signal.emit()

    def Set_Text(self):  # 显示抽取的学习知识
        self.textBrowser.setText(str("{}、".format(self.count + 1)) + self.study_box[self.count][0])


# 知识学习选择板块
    def add_zs(self):   # zs = zhishi
        self.comboBox.addItem("请选择学习内容(如果页面过大或过小，可通过‘ctrl + 鼠标滚轮’调整大小)")  # 添加默认item
        for zs in zhishi_list.zs_ls:
            self.comboBox.addItem(zs)


    def choose_zs(self):   # zs = zhishi
        if self.comboBox.currentIndex() == 0:   # 默认选项时显示空白页
            self.label.setText(self.comboBox.currentText())
            pass
        else:
            self.label.setText(self.comboBox.currentText())
            return self.onOpenFile("./resources/zhishi_file/zhishi{}.docx".format(self.comboBox.currentIndex()))


    def onOpenFile(self, path):
        relative_path = path  # 该文件相对路径
        path = os.path.abspath(relative_path)  # 获取该文件的绝对路径
        return self.openOffice(path, 'Word.Application')


    def openOffice(self, path, app):
        self.axWidget.clear()
        if not self.axWidget.setControl(app):
            return QMessageBox.critical(self, '错误', '没有安装  %s' % app)
        self.axWidget.dynamicCall(
            'SetVisible (bool Visible)', 'false')  # 不显示窗体
        self.axWidget.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        self.axWidget.setProperty('DisplayAlerts', False)
        self.axWidget.setControl(path)
        self.axWidget.show()
        print(path)







if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = Zhishixuexi_Pane()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)