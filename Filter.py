import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from Filter_Calculation import filter
from scipy.interpolate import griddata
from Support import Support_Calculation

class Filter_Calculation(QWidget):
    def __init__(self, parent):
        super(Filter_Calculation, self).__init__(parent)
        self.father = parent
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        self.signal2 = 0
        self.setWindowTitle('反演结果筛选')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 250, 800, 350)

        layoutline1 = QHBoxLayout()
        self.label1 = QLabel('水平梯度滤波法系数1:')
        self.kt1 = QLineEdit()
        layoutline1.addWidget(self.label1, 1)
        layoutline1.addWidget(self.kt1, 1)

        layoutline2 = QHBoxLayout()
        self.label2 = QLabel('水平梯度滤波法系数2:')
        self.kt2 = QLineEdit()
        layoutline2.addWidget(self.label2, 1)
        layoutline2.addWidget(self.kt2, 1)

        layoutline3 = QHBoxLayout()
        self.label3 = QLabel('水平梯度滤波法系数3:')
        self.kt3 = QLineEdit()
        layoutline3.addWidget(self.label3, 1)
        layoutline3.addWidget(self.kt3, 1)

        layoutline4 = QHBoxLayout()
        self.label4 = QLabel('聚散度准则作用半径:')
        self.DS = QLineEdit()
        layoutline4.addWidget(self.label4, 1)
        layoutline4.addWidget(self.DS, 1)

        layoutline5 = QHBoxLayout()
        self.label5 = QLabel('聚散度指数:')
        self.NN = QLineEdit()
        layoutline5.addWidget(self.label5, 1)
        layoutline5.addWidget(self.NN, 1)

        layoutline8 = QHBoxLayout()
        self.checkbox = QCheckBox('结果图中显示边界识别结果')
        self.checkbox.setChecked(False)
        layoutline8.addWidget(self.checkbox, 1)
        self.signal1 = 0

        layoutline7 = QHBoxLayout()
        self.btnsup = QPushButton('辅助线框')
        layoutline7.addWidget(self.btnsup)


        layoutline6 = QHBoxLayout()
        self.button1 = QPushButton('计算并作图')
        self.button2 = QPushButton('取消')
        layoutline6.addWidget(self.button1)
        layoutline6.addWidget(self.button2)

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
        layout1.addLayout(layoutline8, 1)
        layout1.addStretch(1)
        layout1.addLayout(layoutline7, 1)
        layout1.addStretch(2)
        layout1.addLayout(layoutline6, 1)

        layout2 = QVBoxLayout()
        self.label21 = QLabel()
        self.label21.setPixmap(QPixmap('./images/Drawing06.png'))
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
        self.checkbox.stateChanged.connect(self.support1)

    def on_cancel_clicked(self):
        self.close()
        return

    def support(self):
        self.secondui = Support_Calculation(self)
        self.secondui.show()

    def support1(self):
        if self.checkbox.isChecked():
            self.signal1 = 1
        else:
            self.signal1 = 0

    def on_ok_clicked(self):

        if self.kt1.text() =='' or self.kt2.text() =='' or self.kt3.text() =='' or self.DS.text() =='' or self.NN.text() =='':
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
            position = self.father.tab.currentIndex()
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

            x_spacing = (x_e - x_s) / (len_x - 1)
            y_spacing = (y_e - y_s) / (len_y - 1)

            x_spacing = int(x_spacing)
            y_spacing = int(y_spacing)

            kt1 = self.kt1.text()
            kt2 = self.kt2.text()
            kt3 = self.kt3.text()
            DS = self.DS.text()
            NN = self.NN.text()
            kt1 = float(kt1)
            kt2 = float(kt2)
            kt3 = float(kt3)
            DS = float(DS)
            NN = float(NN)

            outx = np.loadtxt('./record/outx.txt')
            outx = outx.astype(float)
            outy = np.loadtxt('./record/outy.txt')
            outy = outy.astype(float)
            outz = np.loadtxt('./record/outz.txt')
            outz = outz.astype(float)
            outn = np.loadtxt('./record/outn.txt')
            outn = outn.astype(float)
            Vxz = np.loadtxt('./record/Vxz.txt')
            Vxz = Vxz.astype(float)
            Vyz = np.loadtxt('./record/Vyz.txt')
            Vyz = Vyz.astype(float)
            Vzz = np.loadtxt('./record/Vzz.txt')
            Vzz = Vzz.astype(float)

            winsize = pd.read_table('./record/winsize.txt', header=None)
            xsize = winsize[0][0]
            xsize = float(xsize)
            ysize = winsize[0][0]
            ysize = float(ysize)

            xunit1 = pd.read_table('./record/xunit.txt', header=None)
            xunit = xunit1[0][0]
            yunit1 = pd.read_table('./record/yunit.txt', header=None)
            yunit = yunit1[0][0]
            zunit1 = pd.read_table('./record/zunit.txt', header=None)
            zunit = zunit1[0][0]

            outputx, outputy, outputz = filter(Vxz, Vyz, Vzz, x, y, x_spacing, y_spacing, outx, outy, outz, outn, xsize, ysize, kt1, kt2, kt3, DS, NN, len_x, len_y)

            zmax = float(outputz.max())
            zmin = float(outputz.min())

            xi = np.linspace(x_s, x_e, len_x, endpoint=True)
            yi = np.linspace(y_s, y_e, len_y, endpoint=True)
            X, Y = np.meshgrid(xi, yi)
            plt.close()
            if self.signal2 == 1:

                rowcount1 = pd.read_table('./record/rowcount.txt', header=None)
                dataset1 = np.loadtxt('./record/range2.txt')
                rowcount = rowcount1[0][0]
                rowcount = int(rowcount)
                dataset1 = dataset1.astype(float)
                dataset1 = dataset1.reshape(rowcount, 6)
                zmin01 = np.argmin(dataset1[:, 4])
                zmin1 = dataset1[zmin01][4]
                zmin1 = int(zmin1 - 1)
                zmax01 = np.argmax(dataset1[:, 5])
                zmax1 = dataset1[zmax01][5]
                zmax1 = int(zmax1 + 1)

                if zmax > zmax1:
                    zmax2 = zmax
                else:
                    zmax2 = zmax1
                if zmin > zmin1:
                    zmin2 = zmin1
                else:
                    zmin2 = zmin

                ax1 = plt.axes(projection='3d')
                if self.signal1 == 1:
                    tempdata = np.loadtxt('./record/Edgeresult.txt')
                    tempdata1 = np.array(tempdata)
                    tempdata2 = tempdata1.astype(float)
                    tempdata3 = tempdata2.reshape(-1)
                    Z = griddata((x, y), tempdata3, (X, Y), method='cubic')
                    ax1.contourf(X, Y, Z, zdir='z', offset=zmin2, alpha=0.5, cmap="viridis")
                ax1.set_title('欧拉反褶积计算结果', fontdict={'size': 12})
                plt.xlabel('x(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
                plt.ylabel('y(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
                ax1.set_zlabel('z(' + str(zunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
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

                outputz0 = outputz * 1
                zmax3 = max(np.unique(outputz0))
                zmin3 = min(np.unique(outputz0))
                zzz = (zmax3 - zmin3) / 5
                for i in range(0, len(outputz0)):
                    if outputz0[i] > zmin3 + 4 * zzz:
                        outputz5.append(outputz0[i])
                        outputy5.append(outputy[i])
                        outputx5.append(outputx[i])
                    elif outputz0[i] > zmin3 + 3 * zzz:
                        outputz4.append(outputz0[i])
                        outputy4.append(outputy[i])
                        outputx4.append(outputx[i])
                    elif outputz0[i] > zmin3 + 2 * zzz:
                        outputz3.append(outputz0[i])
                        outputy3.append(outputy[i])
                        outputx3.append(outputx[i])
                    elif outputz0[i] > zmin3 + zzz:
                        outputz2.append(outputz0[i])
                        outputy2.append(outputy[i])
                        outputx2.append(outputx[i])
                    elif outputz0[i] > zmin3:
                        outputz1.append(outputz0[i])
                        outputy1.append(outputy[i])
                        outputx1.append(outputx[i])

                ax1.scatter(outputx1, outputy1, outputz1, marker='o', color='r', alpha=0.8, s=20,
                            label="<" + str(zmin3 + zzz))
                ax1.scatter(outputx2, outputy2, outputz2, marker='o', color='b', alpha=0.8, s=35,
                            label=str(zmin3 + zzz) + '-' + str(zmin3 + 2 * zzz))
                ax1.scatter(outputx3, outputy3, outputz3, marker='o', color='g', alpha=0.8, s=50,
                            label=str(zmin3 + 2 * zzz) + '-' + str(zmin3 + 3 * zzz))
                ax1.scatter(outputx4, outputy4, outputz4, marker='o', color='y', alpha=0.8, s=65,
                            label=str(zmin3 + 3 * zzz) + '-' + str(zmin3 + 4 * zzz))
                ax1.scatter(outputx5, outputy5, outputz5, marker='o', color='m', alpha=0.8, s=80,
                            label='>' + str(zmin3 + 4 * zzz))
                #ax1.scatter(outputx, outputy, outputz, marker='o')
                ax1.set_xlim(x_s, x_e)
                ax1.set_ylim(y_s, y_e)
                ax1.set_zlim(zmin3, zmax3*1.5)
                ax1.invert_zaxis()

                for i in range(0, rowcount):
                    x1 = dataset1[i][0]
                    x2 = dataset1[i][1]
                    y1 = dataset1[i][2]
                    y2 = dataset1[i][3]
                    z1 = dataset1[i][4]
                    z2 = dataset1[i][5]
                    xdraw = [x2, x2, x2, x2, x1, x1, x1, x1]
                    ydraw = [y1, y2, y2, y1, y1, y2, y2, y1]
                    zdraw = [z2, z2, z1, z1, z2, z2, z1, z1]
                    A0, B0, C0, D0, E0, F0, G0, H0 = zip(xdraw, ydraw, zdraw)

                    lines_1 = zip(A0, B0, C0, D0, A0, E0, F0, G0, H0, D0, C0, G0, H0, E0, F0, B0)

                    ax1.plot3D(*lines_1, c='k')

                plt.show()
                np.savetxt("./record/outputx.txt", outputx)
                np.savetxt("./record/outputy.txt", outputy)
                np.savetxt("./record/outputz.txt", outputz)

                x_s = str(x_s)
                x_e = str(x_e)
                y_s = str(y_s)
                y_e = str(y_e)
                zmin2 = str(zmin2)
                zmax2 = str(zmax2)
                with open('./record/x_s.txt', 'w') as f:
                    f.write(x_s)
                with open('./record/x_e.txt', 'w') as f:
                    f.write(x_e)
                with open('./record/y_s.txt', 'w') as f:
                    f.write(y_s)
                with open('./record/y_e.txt', 'w') as f:
                    f.write(y_e)
                with open('./record/zmin2.txt', 'w') as f:
                    f.write(zmin2)
                with open('./record/zmax2.txt', 'w') as f:
                    f.write(zmax2)

                root = self.father.tree.topLevelItem(position - 1)
                child = QTreeWidgetItem(root)
                child.setText(0, '欧拉反褶积计算结果')
                # 设置树上root为选中状态
                for i in range(0, root.childCount()):
                    root.child(i).setSelected(0)
                child.setSelected(1)
                root.setSelected(0)
                self.close()

            else:
                ax1 = plt.axes(projection='3d')
                if self.signal1 == 1:
                    tempdata = np.loadtxt('./record/Edgeresult.txt')
                    tempdata1 = np.array(tempdata)
                    tempdata2 = tempdata1.astype(float)
                    tempdata3 = tempdata2.reshape(-1)
                    Z = griddata((x, y), tempdata3, (X, Y), method='cubic')
                    ax1.contourf(X, Y, Z, zdir='z', offset=0, alpha=0.5, cmap="viridis")
                ax1.set_title('欧拉反褶积计算结果', fontdict={'size': 12})
                plt.xlabel('x(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
                plt.ylabel('y(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
                ax1.set_zlabel('z(' + str(zunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
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

                outputz0 = outputz * 1
                zmax3 = max(np.unique(outputz0))
                zmin3 = min(np.unique(outputz0))
                zzz = (zmax3 - zmin3)/5
                for i in range(0, len(outputz0)):
                    if outputz0[i] > zmin3 + 4 * zzz:
                        outputz5.append(outputz0[i])
                        outputy5.append(outputy[i])
                        outputx5.append(outputx[i])
                    elif outputz0[i] > zmin3 + 3 * zzz:
                        outputz4.append(outputz0[i])
                        outputy4.append(outputy[i])
                        outputx4.append(outputx[i])
                    elif outputz0[i] > zmin3 + 2 * zzz:
                        outputz3.append(outputz0[i])
                        outputy3.append(outputy[i])
                        outputx3.append(outputx[i])
                    elif outputz0[i] > zmin3 + zzz:
                        outputz2.append(outputz0[i])
                        outputy2.append(outputy[i])
                        outputx2.append(outputx[i])
                    elif outputz0[i] > zmin3:
                        outputz1.append(outputz0[i])
                        outputy1.append(outputy[i])
                        outputx1.append(outputx[i])

                ax1.scatter(outputx1, outputy1, outputz1, marker='o', color='r', alpha=0.8, s=20)#, label="<" + str(zmin3 + zzz))
                ax1.scatter(outputx2, outputy2, outputz2, marker='o', color='b', alpha=0.8, s=30)#, label=str(zmin3 + zzz) + '-' + str(zmin3 + 2 * zzz))
                ax1.scatter(outputx3, outputy3, outputz3, marker='o', color='g', alpha=0.8, s=40)#, label=str(zmin3 + 2 * zzz) + '-' + str(zmin3 + 3 * zzz))
                ax1.scatter(outputx4, outputy4, outputz4, marker='o', color='y', alpha=0.8, s=50)#, label=str(zmin3 + 3 * zzz) + '-' + str(zmin3 + 4 * zzz))
                ax1.scatter(outputx5, outputy5, outputz5, marker='o', color='m', alpha=0.5, s=60)#, label='>' + str(zmin3 + 4 * zzz))

                #ax1.scatter(outputx, outputy, outputz, marker='o')
                ax1.set_xlim(x_s, x_e)
                ax1.set_ylim(y_s, y_e)
                ax1.set_zlim(zmin3, zmax3*1.2)
                ax1.invert_zaxis()

                plt.show()
                np.savetxt("./record/outputx.txt", outputx)
                np.savetxt("./record/outputy.txt", outputy)
                np.savetxt("./record/outputz.txt", outputz)

                x_s = str(x_s)
                x_e = str(x_e)
                y_s = str(y_s)
                y_e = str(y_e)
                zmin = str(zmin)
                zmax = str(zmax)
                with open('./record/x_s.txt', 'w') as f:
                    f.write(x_s)
                with open('./record/x_e.txt', 'w') as f:
                    f.write(x_e)
                with open('./record/y_s.txt', 'w') as f:
                    f.write(y_s)
                with open('./record/y_e.txt', 'w') as f:
                    f.write(y_e)
                with open('./record/zmin2.txt', 'w') as f:
                    f.write(zmin)
                with open('./record/zmax2.txt', 'w') as f:
                    f.write(zmax)

                root = self.father.tree.topLevelItem(position - 1)
                child = QTreeWidgetItem(root)
                child.setText(0, '欧拉反褶积计算结果')
                # 设置树上root为选中状态
                for i in range(0, root.childCount()):
                    root.child(i).setSelected(0)
                child.setSelected(1)
                root.setSelected(0)
                self.close()
