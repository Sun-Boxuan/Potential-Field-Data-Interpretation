from MatplotlibWidget import MatplotlibWidget2
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from scipy.interpolate import griddata
from DEXP import Dexp1
from DEXP import Dexp2
from Support2 import Support_Calculation2

class DEXP_Calculation(QWidget):
    def __init__(self, parent):
        super(DEXP_Calculation, self).__init__(parent)
        self.father = parent

        self.setWindowTitle('DEXP')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 250, 850, 350)
        self.flag = 0
        self.zzmax = 0
        self.zzmin = 0
        self.aa = 0
        self.rr = 0
        self.deepmax =0

        # 界面
        layoutline1 = QHBoxLayout()
        self.label1 = QLabel('数据延拓高度：')
        self.hhighh = QLineEdit()

        layoutline1.addStretch(1)
        layoutline1.addWidget(self.label1, 1)
        layoutline1.addStretch(1)
        layoutline1.addWidget(self.hhighh, 1)
        layoutline1.addStretch(1)

        layoutline2 = QHBoxLayout()
        self.label2 = QLabel('数据延拓层数：')
        self.hhighc = QLineEdit()
        self.hhighc.setValidator(QtGui.QIntValidator())

        layoutline2.addStretch(1)
        layoutline2.addWidget(self.label2, 1)
        layoutline2.addStretch(1)
        layoutline2.addWidget(self.hhighc, 1)
        layoutline2.addStretch(1)

        layoutline3 = QHBoxLayout()
        self.label3 = QLabel('X轴单位')
        self.lexunit = QComboBox(self)
        self.lexunit.addItem('km')
        self.lexunit.addItem('m')
        self.lexunit.setCurrentIndex(1)

        layoutline3.addStretch(1)
        layoutline3.addWidget(self.label3, 1)
        layoutline3.addStretch(1)
        layoutline3.addWidget(self.lexunit, 1)
        layoutline3.addStretch(1)

        layoutline4 = QHBoxLayout()
        self.label4 = QLabel('Y轴单位')
        self.leyunit = QComboBox(self)
        self.leyunit.addItem('km')
        self.leyunit.addItem('m')
        self.leyunit.setCurrentIndex(1)

        layoutline4.addStretch(1)
        layoutline4.addWidget(self.label4, 1)
        layoutline4.addStretch(1)
        layoutline4.addWidget(self.leyunit, 1)
        layoutline4.addStretch(1)

        layoutline5 = QHBoxLayout()
        self.label5 = QLabel('Z轴单位')
        self.lezunit = QComboBox(self)
        self.lezunit.addItem('km')
        self.lezunit.addItem('m')
        self.lezunit.setCurrentIndex(1)

        layoutline5.addStretch(1)
        layoutline5.addWidget(self.label5, 1)
        layoutline5.addStretch(1)
        layoutline5.addWidget(self.lezunit, 1)
        layoutline5.addStretch(1)

        layoutline6 = QHBoxLayout()
        self.rbtn1 = QRadioButton(self)
        self.rbtn2 = QRadioButton(self)
        self.rbtn1.setText('X轴方向剖面')
        self.rbtn2.setText('Y轴方向剖面')
        self.rbtn1.setChecked(True)

        layoutline6.addStretch(1)
        layoutline6.addWidget(self.rbtn1, 1)
        layoutline6.addStretch(1)
        layoutline6.addWidget(self.rbtn2, 1)
        layoutline6.addStretch(1)

        layoutline7 = QHBoxLayout()
        self.label7 = QLabel('成像测线：')
        self.label71 = QLabel('第')
        self.label72 = QLineEdit()
        self.label72.setValidator(QtGui.QIntValidator())
        self.label73 = QLabel('条')
        self.label72.setText('1')

        layoutline7.addStretch(2)
        layoutline7.addWidget(self.label7, 1)
        layoutline7.addStretch(1)
        layoutline7.addWidget(self.label71, 1)
        layoutline7.addWidget(self.label72, 1)
        layoutline7.addWidget(self.label73, 1)
        layoutline7.addStretch(1)

        layoutline9 = QHBoxLayout()
        self.btnsup = QPushButton('深度加权函数')
        layoutline9.addWidget(self.btnsup)

        layoutline8 = QHBoxLayout()
        self.button1 = QPushButton('计算')
        self.button2 = QPushButton('取消')
        layoutline8.addWidget(self.button1)
        layoutline8.addWidget(self.button2)

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
        layout1.addStretch(1)
        layout1.addLayout(layoutline9, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline8, 1)

        layout2 = QVBoxLayout()
        self.label21 = QLabel()
        self.label21.setPixmap(QPixmap('./images/Drawing08.png'))
        layout2.addWidget(self.label21, 1)

        layout = QHBoxLayout()
        layout.addLayout(layout2, 1)
        layout.addLayout(layout1, 1)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        # 信号槽
        self.button1.clicked.connect(self.on_ok_clicked)
        self.button2.clicked.connect(self.on_cancel_clicked)
        self.btnsup.clicked.connect(self.support)

    def on_cancel_clicked(self):
        self.close()
        return

    def support(self):
        self.secondui = Support_Calculation2(self)
        self.secondui.show()

    def on_ok_clicked(self):

        position = self.father.tab.currentIndex()

        if position == 0:
            messageBox = QMessageBox()
            messageBox.setWindowTitle('注意')
            messageBox.setText('请选择正确的文件页')
            messageBox.setStandardButtons(QMessageBox.Yes)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('确定')
            messageBox.exec_()
            if messageBox.clickedButton() == buttonY:
                return

        if self.label1 =='' or self.label2 =='' or self.label72 =='':
            messageBox = QMessageBox()
            messageBox.setWindowTitle('注意')
            messageBox.setText('缺少一些必要参数，\n请继续输入。')
            messageBox.setStandardButtons(QMessageBox.Yes)
            buttonY = messageBox.button(QMessageBox.Yes)
            buttonY.setText('确定')
            messageBox.exec_()
            if messageBox.clickedButton() == buttonY:
                return

        else:
            tableWidget = self.father.tab.widget(position).subWindowList()[0].widget()
            dataset = tableWidget.dataout
            dataset = dataset.astype(float)
            expdeep = int(self.hhighh.text())
            znum = int(self.hhighc.text())
            poumian = int(self.label72.text())
            xunit = self.lexunit.currentText()
            yunit = self.leyunit.currentText()
            zunit = self.lezunit.currentText()

            x = dataset[:, 7]
            y = dataset[:, 8]
            x_s = x[0]
            x_e = x[-1]
            y_s = y[0]
            y_e = y[-1]
            x_s = float(x_s)
            x_e = float(x_e)
            y_s = float(y_s)
            y_e = float(y_e)

            xcount = len(np.unique(x))
            ycount = len(np.unique(y))
            xi = np.linspace(x_s, x_e, xcount)
            yi = np.linspace(y_s, y_e, ycount)
            zi = np.linspace(0, expdeep, znum + 1)
            X, Z1 = np.meshgrid(xi, zi)
            Y, Z2 = np.meshgrid(yi, zi)
            gaunit = 'mGal·m$^0$$^.$$^5$'

            xi2 = np.tile(xi, (znum + 1, 1))
            xi2 = xi2.reshape(-1)
            yi2 = np.tile(yi, (znum + 1, 1))
            yi2 = yi2.reshape(-1)
            zi2 = np.repeat(zi, xcount)
            if self.rbtn1.isChecked():
                mdata1 = Dexp1(dataset, xcount, ycount, expdeep, znum, poumian, x, y, self.flag, self.zzmax, self.zzmin, self.aa, self.rr, self.deepmax)
                mdata = mdata1.reshape(-1, order='F')
                Z = griddata((xi2, zi2), mdata, (X, Z1), method='cubic')
                mw = MatplotlibWidget2()
                mw.mpl.Paint('DEXP', X, Z1, Z, xunit, zunit, gaunit)
                sub = QMdiSubWindow()
                sub.setWidget(mw)
                sub.setWindowTitle('DEXP')
                self.father.tab.widget(position).addSubWindow(sub)
                self.father.tab.widget(position).setActiveSubWindow(sub)
                sub.show()
                # 加节点
                root = self.father.tree.topLevelItem(position - 1)
                child = QTreeWidgetItem(root)
                child.setText(0, 'DEXP')
                # 设置树上root为选中状态
                for i in range(0, root.childCount()):
                    root.child(i).setSelected(0)
                child.setSelected(1)
                root.setSelected(0)
                self.close()

            else:
                mdata2 = Dexp2(dataset, xcount, ycount, expdeep, znum, poumian, x, y, self.flag, self.zzmax, self.zzmin, self.aa, self.rr, self.deepmax)
                mdata = mdata2.reshape(-1, order='F')
                Z = griddata((yi2, zi2), mdata, (Y, Z2), method='cubic')
                mw = MatplotlibWidget2()
                mw.mpl.Paint('DEXP', Y, Z2, Z, yunit, zunit, gaunit, x_label_type='y')
                sub = QMdiSubWindow()
                sub.setWidget(mw)
                sub.setWindowTitle('DEXP')
                self.father.tab.widget(position).addSubWindow(sub)
                self.father.tab.widget(position).setActiveSubWindow(sub)
                sub.show()
                # 加节点
                root = self.father.tree.topLevelItem(position - 1)
                child = QTreeWidgetItem(root)
                child.setText(0, 'DEXP')
                # 设置树上root为选中状态
                for i in range(0, root.childCount()):
                    root.child(i).setSelected(0)
                child.setSelected(1)
                root.setSelected(0)
                self.close()