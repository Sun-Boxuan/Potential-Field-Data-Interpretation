from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Euler import calculateEuler
from RangeTable import ModelWizardWidget
from Regionalexpansion import regional
from matplotlib import pyplot as plt
from scipy.interpolate import griddata
import numpy as np
from Taper2d import taper2d
import pathlib
import pandas as pd

class Euler_Calculation(QWizard):
    def __init__(self, parent):
        super(Euler_Calculation, self).__init__(parent)
        self.father = parent
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.setWindowTitle('联合数据反演')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 150, 1050, 350)

        position = self.father.tab.currentIndex()

        if position == 0:
            QMessageBox.information(self, "注意", "请选择正确的文件页")
            Euler_Calculation.close()

        path = pathlib.Path('./record/pic.png')
        if path.is_file() == False:
            QMessageBox.information(self, "注意", "请先进行边界识别")
            Euler_Calculation.close()
#第一页
        firstPage = QWizardPage()
        firstPage.setSubTitle('物体的数量')
        firstPage.setPixmap(QWizard.WatermarkPixmap, QPixmap('./record/pic.png'))
        layoutline0 = QHBoxLayout()
        self.label0 = QLabel('请输入物体的数量:')
        self.obnum = QLineEdit()
        self.obnum.setValidator(QIntValidator())
        self.obnum.setText('1')

        layoutline0.addWidget(self.label0, 1)
        layoutline0.addWidget(self.obnum, 1)

        firstPage.setLayout(layoutline0)
        firstPage.setCommitPage(1)
#第二页
        secondPage = QWizardPage()
        secondPage.setSubTitle('请输入物体的坐标范围')
        secondPage.setPixmap(QWizard.WatermarkPixmap, QPixmap('./record/pic.png'))
        obnum = int(self.obnum.text())
        self.inputTable = ModelWizardWidget(self, obnum)
        self.layout2 = QVBoxLayout()
        self.layout2.addWidget(self.inputTable, 6)

        secondPage.setLayout(self.layout2)
#第三页
        self.thirdPage = QWizardPage()
        self.thirdPage.setSubTitle('确认物体范围并输入必要参数')
        layoutline1 = QHBoxLayout()
        self.label1 = QLabel('X轴单位')
        self.lexunit = QComboBox()
        self.lexunit.addItem('km')
        self.lexunit.addItem('m')
        self.lexunit.setCurrentIndex(1)
        layoutline1.addWidget(self.label1, 1)
        layoutline1.addWidget(self.lexunit, 1)

        layoutline2 = QHBoxLayout()
        self.label2 = QLabel('Y轴单位')
        self.leyunit = QComboBox()
        self.leyunit.addItem('km')
        self.leyunit.addItem('m')
        self.leyunit.setCurrentIndex(1)
        layoutline2.addWidget(self.label2, 1)
        layoutline2.addWidget(self.leyunit, 1)

        layoutline3 = QHBoxLayout()
        self.label3 = QLabel('Z轴单位')
        self.lezunit = QComboBox()
        self.lezunit.addItem('km')
        self.lezunit.addItem('m')
        self.lezunit.setCurrentIndex(1)
        layoutline3.addWidget(self.label3, 1)
        layoutline3.addWidget(self.lezunit, 1)

        layoutline5 = QHBoxLayout()
        self.label5 = QLabel('计算窗口的尺寸（奇数）:')
        self.winsize = QLineEdit()
        self.winsize.setValidator(QIntValidator())
        layoutline5.addWidget(self.label5, 1)
        layoutline5.addWidget(self.winsize, 1)

        layoutline4 = QHBoxLayout()
        self.checkbox = QCheckBox('结果图中显示边界识别结果')
        self.checkbox.setChecked(False)
        layoutline4.addWidget(self.checkbox, 1)
        self.signal2 = 0

        layoutline6 = QHBoxLayout()
        self.label6 = QLabel('请选择联合计算所需的数据:')
        layoutline6.addWidget(self.label6, 1)

        layoutline7 = QHBoxLayout()
        self.data1 = QComboBox()
        self.data1.addItem('Vxx')
        self.data1.addItem('Vxy')
        self.data1.addItem('Vxz')
        self.data1.addItem('Vyy')
        self.data1.addItem('Vyz')
        self.data1.addItem('Vzz')
        self.data1.addItem('Vz')
        self.data1.setCurrentIndex(2)

        self.data2 = QComboBox()
        self.data2.addItem('Vxx')
        self.data2.addItem('Vxy')
        self.data2.addItem('Vxz')
        self.data2.addItem('Vyy')
        self.data2.addItem('Vyz')
        self.data2.addItem('Vzz')
        self.data2.addItem('Vz')
        self.data2.setCurrentIndex(4)

        self.data3 = QComboBox()
        self.data3.addItem('Vxx')
        self.data3.addItem('Vxy')
        self.data3.addItem('Vxz')
        self.data3.addItem('Vyy')
        self.data3.addItem('Vyz')
        self.data3.addItem('Vzz')
        self.data3.addItem('Vz')
        self.data3.setCurrentIndex(5)

        layoutline7.addWidget(self.data1, 1)
        layoutline7.addStretch(1)
        layoutline7.addWidget(self.data2, 1)
        layoutline7.addStretch(1)
        layoutline7.addWidget(self.data3, 1)

        self.layout3 = QVBoxLayout()
        self.layout3.addLayout(layoutline1, 1)
        self.layout3.addStretch(1)
        self.layout3.addLayout(layoutline2, 1)
        self.layout3.addStretch(1)
        self.layout3.addLayout(layoutline3, 1)
        self.layout3.addStretch(1)
        self.layout3.addLayout(layoutline5, 1)
        self.layout3.addStretch(1)
        self.layout3.addLayout(layoutline4, 1)
        self.layout3.addStretch(1)
        self.layout3.addLayout(layoutline6, 1)
        self.layout3.addStretch(1)
        self.layout3.addLayout(layoutline7, 1)

        self.setWizardStyle(QWizard.ModernStyle)
        self.setPage(1, firstPage)
        self.setPage(2, secondPage)
        self.setPage(3, self.thirdPage)
        self.setStartId(1)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

# 信号槽
        self.currentIdChanged.connect(self.on_currentIdChanged)
        self.finished.connect(self.on_finish_clicked)
        self.checkbox.stateChanged.connect(self.support1)

    def support1(self):
        if self.checkbox.isChecked():
            self.signal2 = 1
        else:
            self.signal2 = 0

    def validateCurrentPage(self):
        id = self.currentId()
        if id == 1:
            if self.obnum.text() == '':
                messageBox = QMessageBox()
                messageBox.setWindowTitle('注意')
                messageBox.setText('请输入物体的数量')
                messageBox.setStandardButtons(QMessageBox.Yes)
                buttonY = messageBox.button(QMessageBox.Yes)
                buttonY.setText('确定')
                messageBox.exec_()
                if messageBox.clickedButton() == buttonY:
                    return 0

            num = int(self.obnum.text())
            if num < 1:
                messageBox = QMessageBox()
                messageBox.setWindowTitle('注意')
                messageBox.setText('请输入一个合理的整数')
                messageBox.setStandardButtons(QMessageBox.Yes)
                buttonY = messageBox.button(QMessageBox.Yes)
                buttonY.setText('确定')
                messageBox.exec_()
                if messageBox.clickedButton() == buttonY:
                    return 0

        if id == 2:
            obnum = int(self.obnum.text())
            for j in range(0, obnum):
                for i in range(0, 4):
                    if self.inputTable.tableWidget.item(j, i).text() == '':
                        messageBox = QMessageBox()
                        messageBox.setWindowTitle('注意')
                        messageBox.setText('缺少一些必要参数，\n请继续输入。')
                        messageBox.setStandardButtons(QMessageBox.Yes)
                        buttonY = messageBox.button(QMessageBox.Yes)
                        buttonY.setText('确定')
                        messageBox.exec_()
                        if messageBox.clickedButton() == buttonY:
                            return 0

        if id == 3:
            if self.winsize.text() == '':
                messageBox = QMessageBox()
                messageBox.setWindowTitle('注意')
                messageBox.setText('请输入计算窗口的尺寸')
                messageBox.setStandardButtons(QMessageBox.Yes)
                buttonY = messageBox.button(QMessageBox.Yes)
                buttonY.setText('确定')
                messageBox.exec_()
                if messageBox.clickedButton() == buttonY:
                    return 0
        return 1

    def on_currentIdChanged(self):
        id = self.currentId()
        if id == 2:
            obnum = int(self.obnum.text())
            self.obnum2 = obnum
            self.inputTable.tableWidget.setRowCount(obnum)
            return
        if id == 3:
            plt.close()
            rowcount = int(self.obnum.text())
            position = self.father.tab.currentIndex()
            dataset_temp = []
            for j in range(0, rowcount):
                for i in range(0, 4):
                    data2 = self.inputTable.tableWidget.item(j, i).text()
                    dataset_temp.append(data2)

            dataset1 = np.array(dataset_temp, dtype=float)
            self.dataset1 = dataset1.reshape(rowcount, 4)
            self.dataset2 = self.dataset1.reshape(-1, 4)
            np.savetxt("./record/range.txt", self.dataset1)
            layout4 = QHBoxLayout()
            # 使用plt通过数据绘图
            tableWidget = self.father.tab.widget(position).subWindowList()[0].widget()
            dataset = tableWidget.dataout
            dataset = dataset.astype('float')

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

            len_x = len(np.unique(x))
            len_y = len(np.unique(y))

            xi = np.linspace(x_s, x_e, len_x, endpoint=True)
            yi = np.linspace(y_s, y_e, len_y, endpoint=True)
            X, Y = np.meshgrid(xi, yi)

            tempdata0 = np.loadtxt('./record/Edgeresult.txt')
            tempdata01 = np.array(tempdata0)
            tempdata02 = tempdata01.astype(float)
            tempdata03 = tempdata02.reshape(-1)

            xunit1 = pd.read_table('./record/xunit1.txt', header=None)
            xunit = xunit1[0][0]
            yunit1 = pd.read_table('./record/yunit1.txt', header=None)
            yunit = yunit1[0][0]
            cunit1 = pd.read_table('./record/zunit1.txt', header=None)
            cunit = cunit1[0][0]

            Z = griddata((x, y), tempdata03, (X, Y), method='cubic')
            fig = plt.figure()
            ax_12_message = fig.add_subplot()
            ax_12_message.set_title('边界识别划定的区域', fontdict={'size': 12})
            plt.xlabel('x(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
            plt.ylabel('y(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
            ax_12_message.contourf(X, Y, Z, cmap='viridis')
            CS = ax_12_message.contourf(X, Y, Z, cmap='viridis')
            plt.colorbar(CS).ax.set_title(str(cunit), fontdict={'family': 'Times New Roman', 'size': 12})
            plt.tight_layout()
            # 绘图划线
            color = ['r', 'c', 'm', 'y', 'k', 'w', 'b', 'g']
            for i in range(0, rowcount):
                x1 = [self.dataset2[i][0], self.dataset2[i][1], self.dataset2[i][1], self.dataset2[i][0], self.dataset2[i][0]]
                y1 = [self.dataset2[i][2], self.dataset2[i][2], self.dataset2[i][3], self.dataset2[i][3], self.dataset2[i][2]]
                plt.plot(x1, y1, color[i])

            fig.savefig("./record/pic1.png")

            self.layout5 = QVBoxLayout()
            self.label51 = QLabel()
            self.label51.setPixmap(QPixmap('./record/pic1.png'))
            self.layout5.addWidget(self.label51, 1)

            layout4.addLayout(self.layout5)#问题在这
            layout4.addLayout(self.layout3)
            self.thirdPage.setLayout(layout4)

    def on_finish_clicked(self):
        if self.currentId() == -1:
            return
        plt.close()

        position = self.father.tab.currentIndex()
        tableWidget = self.father.tab.widget(position).subWindowList()[0].widget()
        dataset = tableWidget.dataout
        dataset = dataset.astype('float')

        xsize = self.winsize.text()
        ysize = self.winsize.text()
        index1 = int(self.data1.currentIndex())
        index2 = int(self.data2.currentIndex())
        index3 = int(self.data3.currentIndex())

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

        len_x = len(np.unique(x))
        len_y = len(np.unique(y))

        x_spacing = (x_e - x_s) / (len_x - 1)
        y_spacing = (y_e - y_s) / (len_y - 1)

        x_spacing = int(x_spacing)
        y_spacing = int(y_spacing)

        Vxz = dataset[:, index1]
        Vyz = dataset[:, index2]
        Vzz = dataset[:, index3]

        Vxz = Vxz.reshape(len_x, len_y)
        Vxz = Vxz.astype(float)
        Vyz = Vyz.reshape(len_x, len_y)
        Vyz = Vyz.astype(float)
        Vzz = Vzz.reshape(len_x, len_y)
        Vzz = Vzz.astype(float)

        (Vxz_y, Vxz_x) = np.gradient(Vxz)
        (Vyz_y, Vyz_x) = np.gradient(Vyz)
        (Vzz_y, Vzz_x) = np.gradient(Vzz)
        Vxyz = (Vxz_y + Vyz_x)/2

        expVxz = taper2d(Vxz, x, y, xsize, ysize, x_spacing, y_spacing)
        expVyz = taper2d(Vyz, x, y, xsize, ysize, x_spacing, y_spacing)
        expVzz = taper2d(Vzz, x, y, xsize, ysize, x_spacing, y_spacing)
        expVxz_x = taper2d(Vxz_x, x, y, xsize, ysize, x_spacing, y_spacing)
        expVyz_y = taper2d(Vyz_y, x, y, xsize, ysize, x_spacing, y_spacing)
        expVzz_x = taper2d(Vzz_x, x, y, xsize, ysize, x_spacing, y_spacing)
        expVzz_y = taper2d(Vzz_y, x, y, xsize, ysize, x_spacing, y_spacing)
        expVxyz = taper2d(Vxyz, x, y, xsize, ysize, x_spacing, y_spacing)
        expx = regional(x, x, y, xsize, ysize, x_spacing, y_spacing)
        expy = regional(y, x, y, xsize, ysize, x_spacing, y_spacing)

        outx, outy, outz, outn = calculateEuler(expVxz, expVyz, expVzz, expVxz_x, expVyz_y, expVzz_x, expVzz_y, expVxyz, xsize, ysize, expx, expy, len_x, len_y)
        np.savetxt("./record/outx.txt", outx)
        np.savetxt("./record/outy.txt", outy)
        np.savetxt("./record/outz.txt", outz)
        np.savetxt("./record/outn.txt", outn)
        np.savetxt("./record/Vxz.txt", Vxz)
        np.savetxt("./record/Vyz.txt", Vyz)
        np.savetxt("./record/Vzz.txt", Vzz)
        np.savetxt("./record/expVxz.txt", expVxz)
        np.savetxt("./record/expVyz.txt", expVyz)
        np.savetxt("./record/expVzz.txt", expVzz)
        outx = outx.reshape(-1)
        outy = outy.reshape(-1)
        outz = outz.reshape(-1)
        zmax = float(np.unique(outz.max()))
        zmin = float(np.unique(outz.min()))
        ax1 = plt.axes(projection='3d')
        if self.signal2 == 1:
            xi = np.linspace(x_s, x_e, len_x, endpoint=True)
            yi = np.linspace(y_s, y_e, len_y, endpoint=True)
            X, Y = np.meshgrid(xi, yi)
            tempdata = np.loadtxt('./record/Edgeresult.txt')
            tempdata1 = np.array(tempdata)
            tempdata2 = tempdata1.astype(float)
            tempdata3 = tempdata2.reshape(-1)
            Z = griddata((x, y), tempdata3, (X, Y), method='cubic')
            ax1.contourf(X, Y, Z, zdir='z', offset=zmin, alpha=0.5, cmap="viridis")
        ax1.set_title('欧拉反褶积计算结果', fontdict={'size': 12})
        plt.xlabel('x(' + str(self.lexunit.currentText()) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.ylabel('y(' + str(self.leyunit.currentText()) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        ax1.set_zlabel('z(' + str(self.lezunit.currentText()) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.tight_layout()

        outputx1 = []
        outputx2 = []
        outputx3 = []
        outputx4 = []
        outputx5 = []

        outputy1 = []
        outputy2 = []
        outputy3 = []
        outputy4 = []
        outputy5 = []

        outputz1 = []
        outputz2 = []
        outputz3 = []
        outputz4 = []
        outputz5 = []

        zzz = (zmax - zmin) / 5
        for i in range(0, len(outz)):
            if outz[i] > zmin + 4 * zzz:
                outputz5.append(outz[i])
                outputy5.append(outy[i])
                outputx5.append(outx[i])
            elif outz[i] > zmin + 3 * zzz:
                outputz4.append(outz[i])
                outputy4.append(outy[i])
                outputx4.append(outx[i])
            elif outz[i] > zmin + 2 * zzz:
                outputz3.append(outz[i])
                outputy3.append(outy[i])
                outputx3.append(outx[i])
            elif outz[i] > zmin + zzz:
                outputz2.append(outz[i])
                outputy2.append(outy[i])
                outputx2.append(outx[i])
            elif outz[i] > zmin:
                outputz1.append(outz[i])
                outputy1.append(outy[i])
                outputx1.append(outx[i])

        ax1.scatter(outputx1, outputy1, outputz1, marker='o', color='r', alpha=0.8, s=20, label="<" + str(zmin + zzz))
        ax1.scatter(outputx2, outputy2, outputz2, marker='o', color='b', alpha=0.8, s=35,
                    label=str(zmin + zzz) + '-' + str(zmin + 2 * zzz))
        ax1.scatter(outputx3, outputy3, outputz3, marker='o', color='g', alpha=0.8, s=50,
                    label=str(zmin + 2 * zzz) + '-' + str(zmin + 3 * zzz))
        ax1.scatter(outputx4, outputy4, outputz4, marker='o', color='y', alpha=0.8, s=65,
                    label=str(zmin + 3 * zzz) + '-' + str(zmin + 4 * zzz))
        ax1.scatter(outputx5, outputy5, outputz5, marker='o', color='m', alpha=0.8, s=80,
                    label='>' + str(zmin + 4 * zzz))
        #ax1.scatter(outx, outy, outz, marker='o')
        ax1.set_xlim(x_s, x_e)
        ax1.set_ylim(y_s, y_e)
        ax1.set_zlim(zmin, zmax)
        ax1.invert_zaxis()
        with open('./record/winsize.txt', 'w') as f:
            f.write(xsize)
        with open('./record/xunit.txt', 'w') as f:
            f.write(str(self.lexunit.currentText()))
        with open('./record/yunit.txt', 'w') as f:
            f.write(str(self.leyunit.currentText()))
        with open('./record/zunit.txt', 'w') as f:
            f.write(str(self.lezunit.currentText()))
        plt.show()

        # 加节点
        root = self.father.tree.topLevelItem(position - 1)
        child = QTreeWidgetItem(root)
        child.setText(0, '欧拉反褶积计算结果')
        # 设置树上root为选中状态
        for i in range(0, root.childCount()):
            root.child(i).setSelected(0)
        child.setSelected(1)
        root.setSelected(0)
        self.close()

