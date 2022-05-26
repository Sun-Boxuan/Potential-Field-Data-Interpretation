import matplotlib
matplotlib.use("Qt5Agg")
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.pyplot import *
import matplotlib.patches as patches

class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure()
        FigureCanvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def Paint(self, title, X, Y, Z, xunit, yunit, colorbarTitle):
        self.fig.suptitle(title, fontdict={'size': 12})
        self.axes.set_xlabel('x(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        self.axes.set_ylabel('y(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})

        # rect1 = patches.Rectangle((200, 100), 200, 200, linewidth=1, edgecolor='r', facecolor='none')
        # self.axes.add_patch(rect1)
        # rect2 = patches.Rectangle((700, 700), 200, 200, linewidth=1, edgecolor='r', facecolor='none')
        # self.axes.add_patch(rect2)

        CS = self.axes.contourf(X, Y, Z, cmap='viridis')
        self.fig.colorbar(CS, shrink=1, aspect=20, label=colorbarTitle, ticklocation='top')
        self.saveFig("./record/pic.png")

    def saveFig(self, fileName):
        self.fig.savefig(fileName)

class MatplotlibWidget(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)

class MyMplCanvas2(FigureCanvas):
    def __init__(self, parent=None):
        # 配置中文显示
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.fig = Figure()
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def Paint(self, title, X, Y, Z, xunit, yunit, colorbarTitle, x_label_type='x', y_label_type='z'):
        self.fig.suptitle(title, fontdict={'size': 12})
        self.axes.set_xlabel(x_label_type+'(' + str(xunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        self.axes.set_ylabel(y_label_type+'(' + str(yunit) + ')', fontdict={'family': 'Times New Roman', 'size': 12})
        self.axes.invert_yaxis()
        CS = self.axes.contourf(X, Y, Z, cmap='viridis')
        self.fig.colorbar(CS, shrink=1, aspect=20, label=colorbarTitle, ticklocation='top')
        self.saveFig("./record/pic.png")

    def saveFig(self, fileName):
        self.fig.savefig(fileName)

class MatplotlibWidget2(QWidget):
    def __init__(self, parent=None):
        super(MatplotlibWidget2, self).__init__(parent)
        self.initUi()

    def initUi(self):
        self.layout = QVBoxLayout(self)
        self.mpl = MyMplCanvas2(self)
        self.mpl_ntb = NavigationToolbar(self.mpl, self)  # 添加完整的 toolbar
        self.layout.addWidget(self.mpl)
        self.layout.addWidget(self.mpl_ntb)