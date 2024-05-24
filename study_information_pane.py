import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from study_information_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal
import matplotlib

from matplotlib import pyplot as plt
import pandas as pd
from matplotlib.font_manager import FontProperties
class Study_Information_Pane(QWidget,Ui_Form):

    show_menu_pane_signal = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(Study_Information_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("学习信息查询页面")

    def study_information_pane_back_menu(self):
        print("返回")
        self.show_menu_pane_signal.emit()


    def enter(self):
        print("确定")
        name = self.lineEdit.text().strip().upper()
        if not name:
            QMessageBox.information(self, "提示", "请输入名字。")
            return

        # 读取日志文件
        try:
            df = pd.read_csv("resources/learning_log.csv", header=0,encoding="utf-8")
            # 去除列名中的空格
            df.columns = [col.replace(" ", "") for col in df.columns]
        except Exception as e:
            QMessageBox.information(self, "错误", f"读取日志文件时出错: {e}")
            return


        # 筛选指定用户名的记录
        df = df[df["用户名"].astype(str).str.strip().str.upper() == name]
        if df.empty:
            QMessageBox.information(self, "提示", "未找到该名字的学习信息。")
            return

        # 计算每个板块的总学习时间
        df["学习时长"] = df["学习时长"].apply(
            lambda x: sum(int(t) * 60 ** i for i, t in enumerate(reversed(x.split(":")))))
        study_time_sum = df.groupby("学习板块")["学习时长"].sum().div(60).round(2)  # 转换为小时并保留两位小数
        print(study_time_sum)
        # 指定中文字体
        plt.rcParams['font.sans-serif'] = ['SimHei']  # 使用黑体
        plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题
        # 绘制条形图


        plt.figure(figsize=(10, 6))
        study_time_sum.plot(kind='bar')

        plt.title(f"学习板块总时间 - {name}")
        plt.xlabel("学习板块")
        plt.ylabel("学习时间 (小时)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        # plt.savefig('test_chart.png')  # 保存图表为图片文件
        # 显示图表
        plt.show()
if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = Study_Information_Pane()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)