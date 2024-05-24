import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from menu_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal
import datetime

class Menu_Pane(QWidget,Ui_Form):

    show_kaoshi_pane_signal = pyqtSignal()
    show_zhishixuexi_pane_signal = pyqtSignal()
    show_chaxun_pane_signal = pyqtSignal()
    show_chemical_learn_pane_signal =pyqtSignal()
    show_study_information_pane_signal =pyqtSignal()
    show_videolearning_pane_signal=pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(Menu_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("菜单界面")
    def update_username(self, name):
        self.username_label.setText(name)  #  self.username_label 是显示用户名的 QLabel
    def zhishixuexi_wd(self):
        print("知识学习")
        self.show_zhishixuexi_pane_signal.emit()

    def kaoshi_wd(self):
        print("考试")
        self.show_kaoshi_pane_signal.emit()

    # def start_kaoshi_time(self):
    #     print("开始记录时间")
    #     self.start_kaoshi_time_signal.emit()
    def videolearning_wd(self):
        print("视频学习")
        self.show_videolearning_pane_signal.emit()

    def chaxun_wd(self):
        print("查询")
        self.show_chaxun_pane_signal.emit()

    def about_wd(self):
        #print("关于")
        QMessageBox.about(self,"关于","""
学校：华南理工大学  
学院：化学与化工学院  
年级：2020级  
专业：制药工程  
毕设：面向不同受众的化学化工知识学习及水平考试系统开发  
姓名：梁桀熙  
Github：https://github.com/Jesse020102/graduation-design  
联系方式：celjx@mail.scut.edu.cn  
导师：方利国  
Github：https://github.com/gzlgfang  
联系方式：lgfang@scut.edu.cn 
""")
    def chemical_wd(self):
        print("chemical")
        self.show_chemical_learn_pane_signal.emit()

    def study_information_wd(self):
        print("信息")
        self.show_study_information_pane_signal.emit()
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = Menu_Pane()

        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)