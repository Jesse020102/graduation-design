import sys
from PyQt5.Qt import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon
import os
from videolearning_ui import Ui_Form
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QListWidget, QStackedWidget, QPushButton,QWidget, QMessageBox, QPushButton,QDesktopWidget
import datetime
class VideoLearning_Pane(QWidget,Ui_Form):
    show_menu_pane_signal = pyqtSignal()
    def __init__(self, parent=None, *args, **kwargs):
        super(VideoLearning_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("视频学习")
        print("运行")
        # 时间模块
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.timeElapsed = QTime()
        # 连接返回按钮的点击事件
        self.pushButton_4.clicked.connect(self.showVideoListPage)
        # 创建视频播放器
        self.videoWidget = QVideoWidget()  # 创建视频播放控件
        self.player = QMediaPlayer()  # 创建媒体播放器
        self.player.setVideoOutput(self.videoWidget)  # 设置视频输出
        # 填充视频列表
        self.populateVideoList()

        # 将videoWidget添加到videoShowPage的布局中
        self.verticalLayout_3.addWidget(self.videoWidget)
        # 连接视频列表的点击事件
        self.videoListWidget.itemClicked.connect(self.playVideo)

    def videolearning_back_menu(self):
        print("返回")

        self.show_menu_pane_signal.emit()


    def onCloseEvent(self, event):
        self.stopTimer()  # 停止计时器
        self.timeElapsed = QTime()  # 重置时间
        self.timeElapsed.start()  # 重新启动时间
        self.time_label.setText("00:00")  # 更新时间显示
        event.accept()  # 接受关闭事件
        print("测试111")
        self.startTimer()  # 重新启动计时器

    def update_username(self,name):
        self.name_label.setText(name)
    def closeEvent(self, event):
        # 停止计时器并获取学习时间
        self.stopTimer()
        elapsed_time = self.timeElapsed.elapsed()
        study_duration = self.time_label.text()

        # 获取学习板块
        study_module = self.study_label.text()

        # # 获取用户名
        username = self.name_label.text()

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
        super(VideoLearning_Pane, self).closeEvent(event)
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

    def populateVideoList(self):
        # 假设这里有一个视频文件列表
        video_files = ['化学实验 一','化学实验 二','化学实验 三','化学实验 四','化学实验 五','化学实验 六','化学实验 七','化学实验 八','化学实验 九','化学实验 十','化学实验 十一','化学实验 十二','化学实验 十三',
            '我们需要化学 第一集', '我们需要化学 第二集','我们需要化学 第三集','我们需要化学 第四集','我们需要化学 第五集','我们需要化学 第六集',]
        for video in video_files:
            listItem = QListWidgetItem(video)
            self.videoListWidget.addItem(listItem)
    def showVideoListPage(self):
        self.stackedWidget.setCurrentWidget(self.videoListPage)

    def handleError(self):

        print(f"Error: {self.player.error()} - {self.player.errorString()}")
    def playVideo(self, item):
        video_url = self.getVideoUrl(item.text())
        print(f"Playing video from: {video_url}")  # 调试输出
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(video_url)))
        self.player.error.connect(self.handleError)  # 连接错误处理信号
        self.player.play()
        # 切换到视频播放页面
        self.stackedWidget.setCurrentWidget(self.videoShowPage)
    def getVideoUrl(self, video_part):
        try:
            video_urls = {
                '化学实验 一': './resources/videos/gzsy_1.mp4',
                '化学实验 二': './resources/videos/gzsy_2.mp4',
                '化学实验 三': './resources/videos/gzsy_3.mp4',
                '化学实验 四': './resources/videos/gzsy_4.mp4',
                '化学实验 五': './resources/videos/gzsy_5.mp4',
                '化学实验 六': './resources/videos/gzsy_6.mp4',
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
                # ... 其他视频部分
            }
            return video_urls.get(video_part, '')
        except:
            print("get有问题")

if __name__ == '__main__':
    app = QApplication([])
    pane = VideoLearning_Pane()
    pane.show()
    app.exec_()