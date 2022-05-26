import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtWidgets import *

class Left_Calculation(QWidget):
    def __init__(self, parent):
        super(Left_Calculation, self).__init__(parent)
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
        z_e = pd.read_table('./record/zmax2.txt', header=None)
        z_e = z_e[0][0]
        z_e = float(z_e)
        z_s = pd.read_table('./record/zmin2.txt', header=None)
        z_s = z_s[0][0]
        z_s = float(z_s)

        outputx = np.loadtxt('./record/outputx.txt')
        outputx = outputx.astype(float)
        outputz = np.loadtxt('./record/outputz.txt')
        outputz = outputz.astype(float)

        xunit1 = pd.read_table('./record/xunit.txt', header=None)
        xunit = xunit1[0][0]
        zunit1 = pd.read_table('./record/zunit.txt', header=None)
        zunit = zunit1[0][0]

        plt.xlabel('x(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.ylabel('z(' + str(zunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        plt.xlim(xmax=x_e, xmin=x_s)
        plt.ylim(ymax=z_s-100, ymin=z_e+100)
        plt.title('X-Z剖面图', fontdict={'size': 12})
        plt.scatter(outputx, outputz, marker='o', color='b')
        plt.show()
        self.close()
