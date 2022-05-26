from MatplotlibWidget import MatplotlibWidget
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from EEDT import calculateEEDT
from scipy.interpolate import griddata

class EEDT_Calculation(QWidget):
    def __init__(self, parent):
        super(EEDT_Calculation, self).__init__(parent)
        self.father = parent

        self.setWindowTitle('改进的方向总水平导数法')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 250, 850, 350)
        # 界面
        layoutline1 = QHBoxLayout()
        self.label2 = QLabel('X轴单位')
        self.lexunit = QComboBox(self)
        self.lexunit.addItem('km')
        self.lexunit.addItem('m')
        self.lexunit.setCurrentIndex(1)

        layoutline1.addStretch(1)
        layoutline1.addWidget(self.label2, 1)
        layoutline1.addStretch(1)
        layoutline1.addWidget(self.lexunit, 1)
        layoutline1.addStretch(1)

        layoutline2 = QHBoxLayout()
        self.label4 = QLabel('Y轴单位')
        self.leyunit = QComboBox(self)
        self.leyunit.addItem('km')
        self.leyunit.addItem('m')
        self.leyunit.setCurrentIndex(1)

        layoutline2.addStretch(1)
        layoutline2.addWidget(self.label4, 1)
        layoutline2.addStretch(1)
        layoutline2.addWidget(self.leyunit, 1)
        layoutline2.addStretch(1)

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
        layout1.addLayout(layoutline4, 1)

        layout2 = QVBoxLayout()
        self.label21 = QLabel()
        self.label21.setPixmap(QPixmap('./images/Drawing05.png'))
        layout2.addWidget(self.label21, 1)

        layout = QHBoxLayout()
        layout.addLayout(layout2, 1)
        layout.addLayout(layout1, 1)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
        # 信号槽
        self.button1.clicked.connect(self.on_ok_clicked)
        self.button2.clicked.connect(self.on_cancel_clicked)

    def on_cancel_clicked(self):
        self.close()
        return

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

        else:
            tableWidget = self.father.tab.widget(position).subWindowList()[0].widget()
            dataset = tableWidget.dataout

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

        numx = len(np.unique(x))
        numy = len(np.unique(y))

        x_spacing = (x_e - x_s) / (numx - 1)
        y_spacing = (y_e - y_s) / (numy - 1)

        x_spacing = int(x_spacing)
        y_spacing = int(y_spacing)

        xunit = self.lexunit.currentText()
        yunit = self.leyunit.currentText()
        gaunit = 'E/m'

        xi = np.linspace(x_s, x_e, numx)
        yi = np.linspace(y_s, y_e, numy)
        X, Y = np.meshgrid(xi, yi)

        EEDT = calculateEEDT(dataset, x_spacing, y_spacing)
        EEDT = EEDT.reshape(-1)

        Z = griddata((x, y), EEDT, (X, Y), method='cubic')

        mw = MatplotlibWidget()
        mw.mpl.Paint('改进的方向总水平导数法', X, Y, Z, xunit, yunit, gaunit)

        np.savetxt("./record/Edgeresult.txt", EEDT)
        with open('./record/xunit1.txt', 'w') as f:
            f.write(str(self.lexunit.currentText()))
        with open('./record/yunit1.txt', 'w') as f:
            f.write(str(self.leyunit.currentText()))
        with open('./record/zunit1.txt', 'w') as f:
            f.write(str(gaunit))

        sub = QMdiSubWindow()
        sub.setWidget(mw)
        sub.setWindowTitle('改进的方向总水平导数法')
        self.father.tab.widget(position).addSubWindow(sub)
        self.father.tab.widget(position).setActiveSubWindow(sub)
        sub.show()
        # 加节点
        root = self.father.tree.topLevelItem(position - 1)
        child = QTreeWidgetItem(root)
        child.setText(0, '改进的方向总水平导数法')
        # 设置树上root为选中状态
        for i in range(0, root.childCount()):
            root.child(i).setSelected(0)
        child.setSelected(1)
        root.setSelected(0)
        self.close()
        return
