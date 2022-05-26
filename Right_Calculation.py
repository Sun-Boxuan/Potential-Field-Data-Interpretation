import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *

class Right_Calculation(QWidget):
    def __init__(self, parent):
        super(Right_Calculation, self).__init__(parent)
        self.father = parent
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
        plt.close()
        y_e = pd.read_table('./record/y_e.txt', header=None)
        y_e = y_e[0][0]
        y_e = float(y_e)
        y_s = pd.read_table('./record/y_s.txt', header=None)
        y_s = y_s[0][0]
        y_s = float(y_s)
        z_e = pd.read_table('./record/zmax2.txt', header=None)
        z_e = z_e[0][0]
        z_e = float(z_e)
        z_s = pd.read_table('./record/zmin2.txt', header=None)
        z_s = z_s[0][0]
        z_s = float(z_s)

        outputy = np.loadtxt('./record/outputy.txt')
        outputy = outputy.astype(float)
        outputz = np.loadtxt('./record/outputz.txt')
        outputz = outputz.astype(float)

        yunit1 = pd.read_table('./record/yunit.txt', header=None)
        yunit = yunit1[0][0]
        zunit1 = pd.read_table('./record/zunit.txt', header=None)
        zunit = zunit1[0][0]

        plt.xlabel('y(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.ylabel('z(' + str(zunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.xlim(xmax=y_e, xmin=y_s)
        plt.ylim(ymax=z_s-100, ymin=z_e+100)
        plt.title('Y-Z剖面图', fontdict={'size': 12})
        plt.scatter(outputy, outputz, marker='o', color='b')
        plt.show()
        self.close()
