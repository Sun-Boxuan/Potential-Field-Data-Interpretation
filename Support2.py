import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class Support_Calculation2(QDialog):
    def __init__(self, parent):
        super(Support_Calculation2, self).__init__(parent)
        self.father = parent
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.setWindowTitle('深度加权函数')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 150, 350, 350)

        layoutline1 = QHBoxLayout()
        self.label1 = QLabel('地质体顶部深度：')
        self.high1 = QLineEdit()

        layoutline1.addStretch(1)
        layoutline1.addWidget(self.label1, 1)
        layoutline1.addStretch(1)
        layoutline1.addWidget(self.high1, 1)
        layoutline1.addStretch(1)

        layoutline2 = QHBoxLayout()
        self.label2 = QLabel('地质体底部深度：')
        self.high2 = QLineEdit()

        layoutline2.addStretch(1)
        layoutline2.addWidget(self.label2, 1)
        layoutline2.addStretch(1)
        layoutline2.addWidget(self.high2, 1)
        layoutline2.addStretch(1)

        layoutline3 = QHBoxLayout()
        self.label3 = QLabel('参数r：        ')
        self.rr = QLineEdit()

        layoutline3.addStretch(1)
        layoutline3.addWidget(self.label3, 1)
        layoutline3.addStretch(1)
        layoutline3.addWidget(self.rr, 1)
        layoutline3.addStretch(1)

        layoutline4 = QHBoxLayout()
        self.label4 = QLabel('参数α：       ')
        self.aa = QLineEdit()

        layoutline4.addStretch(1)
        layoutline4.addWidget(self.label4, 1)
        layoutline4.addStretch(1)
        layoutline4.addWidget(self.aa, 1)
        layoutline4.addStretch(1)

        layoutline5 = QHBoxLayout()
        self.label5 = QLabel('场地最大深度  ：')
        self.lar = QLineEdit()

        layoutline5.addStretch(1)
        layoutline5.addWidget(self.label5, 1)
        layoutline5.addStretch(1)
        layoutline5.addWidget(self.lar, 1)
        layoutline5.addStretch(1)

        layoutline6 = QHBoxLayout()
        self.checkbox = QCheckBox('引入深度加权函数')
        self.checkbox.setChecked(False)
        layoutline6.addStretch(1)
        layoutline6.addWidget(self.checkbox, 5)
        layoutline6.addStretch(1)

        layoutline7 = QHBoxLayout()
        self.button1 = QPushButton('退出')
        layoutline7.addWidget(self.button1)

        layout1 = QVBoxLayout()
        layout1.addStretch(1)
        layout1.addLayout(layoutline1, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline2, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline3, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline4, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline5, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline6, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline7, 1)

        layout = QHBoxLayout()
        layout.addLayout(layout1, 1)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        self.button1.clicked.connect(self.on_cancel_clicked)

    def on_cancel_clicked(self):
        if self.checkbox.isChecked():
            self.father.flag = 1
            self.father.zzmax = float(self.high2.text())
            self.father.zzmin = float(self.high1.text())
            self.father.aa = float(self.aa.text())
            self.father.rr = float(self.rr.text())
            self.father.deepmax = float(self.lar.text())
        self.close()