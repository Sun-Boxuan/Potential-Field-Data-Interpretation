import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from scipy.interpolate import griddata
from MatplotlibWidget import MatplotlibWidget


class ImageCreateEquipotential(QWidget):
    def __init__(self, parent):
        super(ImageCreateEquipotential, self).__init__(parent)
        self.father = parent

        self.setWindowTitle('网格图')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 250, 700, 350)
#界面
        layoutline1 = QHBoxLayout()
        self.label2 = QLabel('X轴单位：')
        self.lexunit = QComboBox(self)
        self.lexunit.addItem('km')
        self.lexunit.addItem('m')
        self.lexunit.setCurrentIndex(1)

        layoutline1.addWidget(self.label2, 1)
        layoutline1.addWidget(self.lexunit, 1)

        layoutline2 = QHBoxLayout()
        self.label4 = QLabel('Y轴单位：')
        self.leyunit = QComboBox(self)
        self.leyunit.addItem('km')
        self.leyunit.addItem('m')
        self.leyunit.setCurrentIndex(1)

        layoutline2.addWidget(self.label4, 1)
        layoutline2.addWidget(self.leyunit, 1)

        layoutline3 = QHBoxLayout()
        self.label5 = QLabel('重力梯度单位:')
        self.leggunit = QComboBox(self)
        self.leggunit.addItem('E')
        self.leggunit.addItem('g/cm^3')
        self.leggunit.setCurrentIndex(0)

        layoutline3.addWidget(self.label5, 1)
        layoutline3.addWidget(self.leggunit, 1)

        layoutline5 = QHBoxLayout()
        self.label6 = QLabel('重力异常单位:')
        self.legaunit = QComboBox(self)
        self.legaunit.addItem('g.u.')
        self.legaunit.addItem('m/s^2')
        self.legaunit.addItem('mGal')
        self.legaunit.setCurrentIndex(2)

        layoutline5.addWidget(self.label6, 1)
        layoutline5.addWidget(self.legaunit, 1)

        layoutline4 = QHBoxLayout()
        self.button1 = QPushButton('作图')
        self.button2 = QPushButton('取消')
        layoutline4.addWidget(self.button1)
        layoutline4.addWidget(self.button2)

        layout1 = QVBoxLayout()
        layout1.addStretch(1)
        layout1.addLayout(layoutline1, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline2, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline3, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline5, 1)
        layout1.addStretch(2)
        layout1.addLayout(layoutline4, 1)

        layout2 = QVBoxLayout()
        self.label21 = QLabel()
        self.label21.setPixmap(QPixmap('./images/Drawing04.png'))
        layout2.addWidget(self.label21, 1)

        layout = QHBoxLayout()
        layout.addLayout(layout2, 1)
        layout.addLayout(layout1, 1)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
#信号槽
        self.button1.clicked.connect(self.on_ok_clicked)
        self.button2.clicked.connect(self.on_cancel_clicked)


    def on_cancel_clicked(self):
        self.close()
        return

    def on_ok_clicked(self):
# 获取当读取的文件内容
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

        tableWidget = self.father.tab.widget(position).subWindowList()[0].widget()
        dataset = tableWidget.dataout

        Vxx = dataset[:, 0]
        Vxy = dataset[:, 1]
        Vxz = dataset[:, 2]
        Vyy = dataset[:, 3]
        Vyz = dataset[:, 4]
        Vzz = dataset[:, 5]
        Vz = dataset[:, 6]
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

        x_spacing = (x_e - x_s)/(xcount - 1)
        y_spacing = (y_e - y_s)/(ycount - 1)
        x_spacing = int(x_spacing)
        y_spacing = int(y_spacing)

        xunit = self.lexunit.currentText()
        yunit = self.leyunit.currentText()
        ggunit = self.leggunit.currentText()
        gaunit = self.legaunit.currentText()

        xi = np.linspace(x_s, x_e, x_spacing)
        yi = np.linspace(y_s, y_e, y_spacing)
        X, Y = np.meshgrid(xi, yi)

        Zxx = griddata((x, y), Vxx, (X, Y), method='cubic')
        mw1 = MatplotlibWidget()
        mw1.mpl.Paint('Vxx', X, Y, Zxx, xunit, yunit, ggunit)
        sub1 = QMdiSubWindow()
        sub1.setWidget(mw1)
        sub1.setWindowTitle(ggunit)
        self.father.tab.widget(position).addSubWindow(sub1)
        sub1.show()

        Zxy = griddata((x, y), Vxy, (X, Y), method='cubic')
        mw2 = MatplotlibWidget()
        mw2.mpl.Paint('Vxy', X, Y, Zxy, xunit, yunit, ggunit)
        sub2 = QMdiSubWindow()
        sub2.setWidget(mw2)
        sub2.setWindowTitle(ggunit)
        self.father.tab.widget(position).addSubWindow(sub2)
        sub2.show()

        Zxz = griddata((x, y), Vxz, (X, Y), method='cubic')
        mw3 = MatplotlibWidget()
        mw3.mpl.Paint('Vxz', X, Y, Zxz, xunit, yunit, ggunit)
        sub3 = QMdiSubWindow()
        sub3.setWidget(mw3)
        sub3.setWindowTitle(ggunit)
        self.father.tab.widget(position).addSubWindow(sub3)
        sub3.show()

        Zyy = griddata((x, y), Vyy, (X, Y), method='cubic')
        mw4 = MatplotlibWidget()
        mw4.mpl.Paint('Vyy', X, Y, Zyy, xunit, yunit, ggunit)
        sub4 = QMdiSubWindow()
        sub4.setWidget(mw4)
        sub4.setWindowTitle(ggunit)
        self.father.tab.widget(position).addSubWindow(sub4)
        sub4.show()

        Zyz = griddata((x, y), Vyz, (X, Y), method='cubic')
        mw5 = MatplotlibWidget()
        mw5.mpl.Paint('Vyz', X, Y, Zyz, xunit, yunit, ggunit)
        sub5 = QMdiSubWindow()
        sub5.setWidget(mw5)
        sub5.setWindowTitle(ggunit)
        self.father.tab.widget(position).addSubWindow(sub5)
        sub5.show()

        Zzz = griddata((x, y), Vzz, (X, Y), method='cubic')
        mw6 = MatplotlibWidget()
        mw6.mpl.Paint('Vzz', X, Y, Zzz, xunit, yunit, ggunit)
        sub6 = QMdiSubWindow()
        sub6.setWidget(mw6)
        sub6.setWindowTitle(ggunit)
        self.father.tab.widget(position).addSubWindow(sub6)
        sub6.show()

        Zz = griddata((x, y), Vz, (X, Y), method='cubic')
        mw7 = MatplotlibWidget()
        mw7.mpl.Paint('Vz', X, Y, Zz, xunit, yunit, gaunit)
        sub7 = QMdiSubWindow()
        sub7.setWidget(mw7)
        sub7.setWindowTitle(gaunit)
        self.father.tab.widget(position).addSubWindow(sub7)
        sub7.show()

        self.father.tab.widget(position).setActiveSubWindow(sub7)

        # 树加节点
        root = self.father.tree.topLevelItem(position - 1)
        child1 = QTreeWidgetItem(root)
        child1.setText(0, 'Vxx')

        child2 = QTreeWidgetItem(root)
        child2.setText(0, 'Vxy')

        child3 = QTreeWidgetItem(root)
        child3.setText(0, 'Vxz')

        child4 = QTreeWidgetItem(root)
        child4.setText(0, 'Vyy')

        child5 = QTreeWidgetItem(root)
        child5.setText(0, 'Vyz')

        child6 = QTreeWidgetItem(root)
        child6.setText(0, 'Vzz')

        child7 = QTreeWidgetItem(root)
        child7.setText(0, 'Vz')
        # 设置树上root为选中状态
        for i in range(0, root.childCount()):
            root.child(i).setSelected(0)

        child7.setSelected(1)
        root.setSelected(0)
        self.close()

