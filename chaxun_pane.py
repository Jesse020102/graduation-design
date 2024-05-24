import sys
from PyQt5.Qt import *
from PyQt5.QtWidgets import QWidget, QMessageBox, QPushButton
from chaxun_ui import Ui_Form
from PyQt5.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QAbstractAnimation, QEasingCurve, pyqtSignal
import pandas as pd
class Chaxun_Pane(QWidget,Ui_Form):

    show_menu_pane_signal = pyqtSignal()

    def __init__(self, parent=None, *args, **kwargs):
        super(Chaxun_Pane, self).__init__(parent, *args, **kwargs)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setupUi(self)
        self.setWindowTitle("查询页面")
        self.pushButton.clicked.connect(self.on_search)
        self.data = pd.read_excel('resources/search_data.xlsx')
    def on_search(self):
        search_query = self.textEdit.toPlainText()
        if search_query:
            # 进行模糊查询
            filtered_data = self.data[
                self.data.apply(lambda row: row.astype(str).str.contains(search_query, case=False, na=False).any(),axis=1)]
            if not filtered_data.empty:
                # 显示查询结果
                self.textBrowser.setText(filtered_data['CAS登录号'].iloc[0])  # 列名为 'CAS登录号'
                self.textBrowser_2.setText(filtered_data['中文名'].iloc[0])  # 列名为 '中文名'
                self.textBrowser_3.setText(filtered_data['分子式'].iloc[0])  # 列名为 '分子式'
                self.textBrowser_4.setText(filtered_data['英文名'].iloc[0])  # 列名为 '英文名'

                cas_number =filtered_data['CAS登录号'].iloc[0]
                image_filename="resources/chaxun_image/"+cas_number+".jpg"
                self.load_image(image_filename)
            else:
                QMessageBox.information(self, "提示", "未找到相关信息。")

    def load_image(self, image_filename):
        pixmap = QPixmap(image_filename)
        if not pixmap.isNull():
            self.picture_label.setPixmap(pixmap)
            self.picture_label.setScaledContents(True)  # 需要图片自适应 QLabel 大小
        else:
            QMessageBox.information(self, "错误", "无法加载图片。")

    def chaxun_back_menu(self):
        print("返回")
        self.show_menu_pane_signal.emit()



if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        w = Chaxun_Pane()
        w.show()
        sys.exit(app.exec_())
    except Exception as e:
        print("Exception:", e)