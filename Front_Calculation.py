import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *

class Front_Calculation(QWidget):
    def __init__(self, parent):
        super(Front_Calculation, self).__init__(parent)
        self.father = parent
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.close()
        x_e = pd.read_table('./record/x_e.txt', header=None)
        x_e = x_e[0][0]
        x_e = float(x_e)
        x_s = pd.read_table('./record/x_s.txt', header=None)
        x_s = x_s[0][0]
        x_s = float(x_s)
        y_e = pd.read_table('./record/y_e.txt', header=None)
        y_e = y_e[0][0]
        y_e = float(y_e)
        y_s = pd.read_table('./record/y_s.txt', header=None)
        y_s = y_s[0][0]
        y_s = float(y_s)

        outputx = np.loadtxt('./record/outputx.txt')
        outputx = outputx.astype(float)
        outputy = np.loadtxt('./record/outputy.txt')
        outputy = outputy.astype(float)
        outputz = np.loadtxt('./record/outputz.txt')
        outputz = outputz.astype(float)

        xunit1 = pd.read_table('./record/xunit.txt', header=None)
        xunit = xunit1[0][0]
        yunit1 = pd.read_table('./record/yunit.txt', header=None)
        yunit = yunit1[0][0]

        plt.xlabel('x(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.ylabel('y(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.xlim(xmax=x_e, xmin=x_s)
        plt.ylim(ymax=y_e, ymin=y_s)
        plt.title('X-Y剖面图', fontdict={'size': 12})
        #plt.scatter(outputx, outputy, marker='o', color='b')

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
        outputz0 = outputz * 1.1
        zmax2 = max(outputz0)
        zmin2 = min(outputz0)
        zzz = (zmax2 - zmin2) / 5
        for i in range(0, len(outputz0)):
            if outputz0[i] > zmin2 + 4 * zzz:
                outputz5.append(outputz0[i])
                outputy5.append(outputy[i])
                outputx5.append(outputx[i])
            elif outputz0[i] > zmin2 + 3 * zzz:
                outputz4.append(outputz0[i])
                outputy4.append(outputy[i])
                outputx4.append(outputx[i])
            elif outputz0[i] > zmin2 + 2 * zzz:
                outputz3.append(outputz0[i])
                outputy3.append(outputy[i])
                outputx3.append(outputx[i])
            elif outputz0[i] > zmin2 + zzz:
                outputz2.append(outputz0[i])
                outputy2.append(outputy[i])
                outputx2.append(outputx[i])
            elif outputz0[i] > zmin2:
                outputz1.append(outputz0[i])
                outputy1.append(outputy[i])
                outputx1.append(outputx[i])

        plt.scatter(outputx1, outputy1, marker='o', color='r', alpha=0.8, s=20)
        plt.scatter(outputx2, outputy2, marker='o', color='b', alpha=0.8, s=35)
        plt.scatter(outputx3, outputy3, marker='o', color='g', alpha=0.8, s=50)
        plt.scatter(outputx4, outputy4, marker='o', color='y', alpha=0.8, s=65)
        plt.scatter(outputx5, outputy5, marker='o', color='m', alpha=0.8, s=80)

        plt.show()
        self.close()
