import datetime
import sys
from menu_pane import Menu_Pane
from kaoshi_pane import Kaoshi_Pane
from zhishixuexi_pane import Zhishixuexi_Pane
from login_pane import Login_Pane
from PyQt5.Qt import *
from chaxun_pane import Chaxun_Pane
from videolearning_pane import VideoLearning_Pane
from study_information_pane import  Study_Information_Pane
from chemical_learn_pane import  Chemical_Learn_Pane



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        username = ""
        #定义变量
        login_pane = Login_Pane()
        menu_pane = Menu_Pane()
        kaoshi_pane = Kaoshi_Pane()
        zhishixuexi_pane = Zhishixuexi_Pane()
        chaxun_pane =Chaxun_Pane()
        videolearning_pane = VideoLearning_Pane()
        study_information_pane = Study_Information_Pane()
        chemical_learn_pane = Chemical_Learn_Pane()
        login_pane.show()

        #登录按钮，登录进入菜单



        # def start_kaoshi_time():
        #     print("开始考试")
        #     start_time=datetime.datetime.now()
        def handle_username(name):
            global username
            username = name  # 保存用户名
            menu_pane.update_username(name)  # 更新菜单界面的用户名

            show_menu_pane()  # 显示菜单界面
        def handle_username1(name):
            zhishixuexi_pane.update_username(name)
        def handle_username2(name):
            chemical_learn_pane.update_username(name)

        def show_kaoshi_pane():

            kaoshi_pane.show()
            menu_pane.hide()

        def show_zhishixuexi_pane():
            zhishixuexi_pane.update_username1(username)  # 更新知识学习界面的用户名
            zhishixuexi_pane.show()
            menu_pane.hide()
        def show_chaxun_pane():
            chaxun_pane.show()
            menu_pane.hide()


        def show_menu_pane():
            menu_pane.show()
            zhishixuexi_pane.hide()
            kaoshi_pane.hide()
            chemical_learn_pane.hide()
            videolearning_pane.hide()
            login_pane.hide()

        def show_videolearning_pane():
            menu_pane.hide()
            videolearning_pane.show()
            videolearning_pane.update_username(username)
        def show_study_information_pane():
            study_information_pane.show()
            menu_pane.hide()


        def show_chemical_learn_pane():
            chemical_learn_pane.show()
            menu_pane.hide()
            chemical_learn_pane.update_username1(username)  # 更新知识学习界面的用户名
        #信号
        login_pane.login_signal.connect(lambda:show_menu_pane())#从登录跳转菜单
        menu_pane.show_kaoshi_pane_signal.connect(lambda:show_kaoshi_pane())
        menu_pane.show_zhishixuexi_pane_signal.connect(lambda :show_zhishixuexi_pane())
        menu_pane.show_chaxun_pane_signal.connect(lambda :show_chaxun_pane())

        zhishixuexi_pane.show_menu_pane_signal.connect(lambda :show_menu_pane())
        kaoshi_pane.show_menu_pane_signal.connect(lambda: show_menu_pane())
        chaxun_pane.show_menu_pane_signal.connect(lambda: show_menu_pane())
        login_pane.pass_name_signal.connect(handle_username)
        login_pane.pass_name_signal.connect(handle_username)
        videolearning_pane.show_menu_pane_signal.connect(lambda: show_menu_pane())
        menu_pane.show_videolearning_pane_signal.connect(lambda:show_videolearning_pane())
        study_information_pane.show_menu_pane_signal.connect(lambda: show_menu_pane())
        menu_pane.show_study_information_pane_signal.connect(lambda: show_study_information_pane())
        chemical_learn_pane.show_menu_pane_signal.connect(lambda: show_menu_pane())
        menu_pane.show_chemical_learn_pane_signal.connect(lambda: show_chemical_learn_pane())


        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)

