
import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from login_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal

class Login_Pane(QWidget,Ui_Form):

    login_signal=pyqtSignal()
    pass_name_signal=pyqtSignal(str)
    def __init__(self, parent=None, *args, **kwargs):
        super(Login_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("登陆界面")

    def login_back_menu(self):
        # print("登录成功")
        self.login_signal.emit()


    def pass_name(self):
        name=self.lineEdit.text()
        self.pass_name_signal.emit(name)
    def exit_login(self):
        print("退出成功")
        exit()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = Login_Pane()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)


