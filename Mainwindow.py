import sys
import numpy as np
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from Filter import Filter_Calculation
from Tree import TreeWidget
from OpenWizard import OpenWizard
from ImageCreate import ImageCreateEquipotential
from Wavelettransform import Wavelettransform
from Wavelettransform2 import Wavelettransform2
from ED_ACalculation import ED_ACalculation
from AS_Calculation import AS_Calculation
from TILT_Calculation import TILT_Calculation
from Theta_Calculation import Theta_Calculation
from EDT_Calculation import EDT_Calculation
from NEDT_Calculation import NEDT_Calculation
from EEDT_Calculation import EEDT_Calculation
from RRR_Calculation import RRR_Calculation
from NEEDT_Calculation import NEEDT_Calculation
from EAS_Calculation import EAS_Calculation
from Euler_Calculation import Euler_Calculation
from Front_Calculation import Front_Calculation
from Left_Calculation import Left_Calculation
from Right_Calculation import Right_Calculation
from THDR_Calculation import THDR_Calculation
from DEXP_Calculation import DEXP_Calculation

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("位场数据处理解释软件")
        self.status = self.statusBar()
        self.showMaximized()#窗口最大化
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))

#菜单栏部分
        bar = self.menuBar()
        file = bar.addMenu('文件')#文件
        openAction = QAction(QIcon('./images/open.jpg'), '打开文件', self)
        openAction.setShortcut("Ctrl+O")
        file.addAction(openAction)
        saveAction = QAction(QIcon('./images/save.jpg'), '保存当前文件', self)
        saveAction.setShortcut("Ctrl+S")
        file.addAction(saveAction)
        closeAction = QAction(QIcon("./images/close.jpg"), "关闭当前文件", self)
        file.addAction(closeAction)
        quitAction = QAction(QIcon("./images/quit.jpg"), "退出软件", self)
        file.addAction(quitAction)

        image = bar.addMenu('绘图')#绘图
        Gravity_image = QAction('等值线图', self)
        image.addAction(Gravity_image)

        noiseremoval = bar.addMenu('消除噪声')
        Wavelet = QAction('小波变换', self)
        Wavelet2 = QAction('小波变换+Sigma', self)
        noiseremoval.addAction(Wavelet)
        noiseremoval.addAction(Wavelet2)

        edge = bar.addMenu('边界识别')  # 边界识别

        EDGE_menu = QMenu('边界识别', self)
        ED_A = QAction('水平导数法', self)
        AS = QAction('解析信号法', self)
        TILT = QAction('倾斜角法', self)
        THDR = QAction('总水平导数法', self)
        EDT = QAction('方向总水平导数法', self)
        NEDT = QAction('归一化方向总水平导数法', self)
        EEDT = QAction('改进的方向总水平导数法', self)
        RRR = QAction('相关系数法', self)
        NEEDT = QAction('归一化的改进方向总水平导数法', self)
        EAS = QAction('EASM-R', self)

        edge.addAction(ED_A)
        edge.addAction(AS)
        edge.addAction(TILT)
        edge.addAction(EDT)
        edge.addAction(NEDT)
        edge.addAction(EEDT)
        edge.addAction(THDR)
        edge.addAction(RRR)
        edge.addAction(NEEDT)
        edge.addAction(EAS)

        calculate = bar.addMenu('欧拉反褶积计算')
        EDGE_menu.addAction(ED_A)
        EDGE_menu.addAction(AS)
        EDGE_menu.addAction(TILT)
        EDGE_menu.addAction(EDT)
        EDGE_menu.addAction(NEDT)
        EDGE_menu.addAction(EEDT)
        EDGE_menu.addAction(THDR)
        EDGE_menu.addAction(RRR)
        EDGE_menu.addAction(NEEDT)
        EDGE_menu.addAction(EAS)
        calculate.addMenu(EDGE_menu)

        Euler_menu = QAction('联合数据反演', self)
        calculate.addAction(Euler_menu)

        Filter_menu = QAction('反演结果筛选', self)
        calculate.addAction(Filter_menu)

        Profile_menu = QMenu('剖面图', self)
        Front_P = QAction('X-Y剖面图', self)
        Left_P = QAction('X-Z剖面图', self)
        Right_P = QAction('Y-Z剖面图', self)

        Profile_menu.addAction(Front_P)
        Profile_menu.addAction(Left_P)
        Profile_menu.addAction(Right_P)
        calculate.addMenu(Profile_menu)

        DEXP = QAction('DEXP', self)
        TDcalculate = bar.addMenu('三维成像')
        TDcalculate.addAction(DEXP)

        about = bar.addMenu('关于')#关于
        About_message = QAction('信息', self)
        about.addAction(About_message)
#工具栏快捷键
        tb = self.addToolBar("File")
        tb.addAction(openAction)
        tb.addAction(saveAction)
        tb.addAction(quitAction)
#TableWidget
        self.tableWidget = QTableWidget()
# 树
        self.dockWidget = QDockWidget("文件树", self)
        self.dockWidget.setAllowedAreas(Qt.LeftDockWidgetArea)
        self.dockWidget.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.tree = TreeWidget(self)
        self.tree.setColumnCount(1)
        self.tree.setHeaderLabels(['文件'])
        self.tree.setColumnWidth(0, 300)
        self.dockWidget.setWidget(self.tree)  # 将文件树加入到停靠窗口
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dockWidget)  # 将停靠窗口加入到主窗口
#Tab
        self.tab = QTabWidget()#主标签页
        self.welcome = QLabel(self)
        self.widget = QWidget()
        pixmap = QPixmap("./images/Mainwindow.back.jpeg")
        self.welcome.setPixmap(pixmap)
        self.welcome.setAlignment(Qt.AlignCenter)
        self.tab.addTab(self.welcome, "欢迎使用")
        self.setCentralWidget(self.tab)
#信号槽
        quitAction.triggered.connect(self.Quit1)
        openAction.triggered.connect(self.open)
        About_message.triggered.connect(self.About_message1)
        saveAction.triggered.connect(self.Save)
        closeAction.triggered.connect(self.closetab)

        Gravity_image.triggered.connect(self.Gravity_image)

        Wavelet.triggered.connect(self.Wavelet)
        Wavelet2.triggered.connect(self.Wavelet2)

        ED_A.triggered.connect(self.ED_A)
        AS.triggered.connect(self.AS)
        TILT.triggered.connect(self.TILT)
        EDT.triggered.connect(self.EDT)
        NEDT.triggered.connect(self.NEDT)
        EEDT.triggered.connect(self.EEDT)
        NEEDT.triggered.connect(self.NEEDT)
        RRR.triggered.connect(self.RRR)
        THDR.triggered.connect(self.THDR)
        EAS.triggered.connect(self.EAS)

        Euler_menu.triggered.connect(self.Euler)
        Filter_menu.triggered.connect(self.Filter)

        Front_P.triggered.connect(self.Front_P)
        Left_P.triggered.connect(self.Left_P)
        Right_P.triggered.connect(self.Right_P)

        DEXP.triggered.connect(self.Dexp)

        self.tree.clicked.connect(self.onTreeClicked)
        self.tab.currentChanged.connect(self.onCurrentChanged)  # 点击Tab标签
#槽函数
    def Quit1(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle('注意')
        messageBox.setText('你确定要退出？')
        messageBox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        buttonN = messageBox.button(QMessageBox.No)
        buttonN.setText('取消')
        messageBox.exec_()

        if messageBox.clickedButton() == buttonY:
            self.close()
        else:
            return

    def closetab(self):
        position = self.tab.currentIndex()
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
            # 获取索引
            position = self.tab.currentIndex()
            # 删除tab页
            self.tab.removeTab(position)
            # 删除文件树
            self.tree.takeTopLevelItem(position - 1)

    def Save(self):
        position = self.tab.currentIndex()

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
            tableWidget = self.tab.widget(position).subWindowList()[0].widget()
            dataset_n = tableWidget.dataout

            dataset_n = dataset_n.astype('float64')
            dirpath = QFileDialog.getSaveFileName(self, '请选择文件储存的路径', 'C:\\Users\\Desktop\\', 'txt(*.txt)')

            if dirpath[0] == '':
                return

            else:
                np.savetxt(dirpath[0], dataset_n, fmt='%f', delimiter=',')
                messageBox = QMessageBox()
                messageBox.setWindowTitle('提示')
                messageBox.setText('文件储存成功')
                messageBox.setStandardButtons(QMessageBox.Yes)
                buttonY = messageBox.button(QMessageBox.Yes)
                buttonY.setText('确定')
                messageBox.exec_()
                if messageBox.clickedButton() == buttonY:
                    return

    def open(self):
        openwizard = OpenWizard(self)
        openwizard.show()
        return

    def About_message1(self):
        messageBox = QMessageBox()
        messageBox.setWindowTitle('软件信息')
        messageBox.setText('软件开发完成时间：2022.03.20')
        messageBox.setStandardButtons(QMessageBox.Yes)
        buttonY = messageBox.button(QMessageBox.Yes)
        buttonY.setText('确定')
        messageBox.exec_()
        if messageBox.clickedButton() == buttonY:
            return

    def Gravity_image(self):
        image_creat = ImageCreateEquipotential(self)
        image_creat.show()
        return

    def Wavelet(self):
        wavelet = Wavelettransform(self)
        wavelet.show()
        return

    def Wavelet2(self):
        wavelet2 = Wavelettransform2(self)
        wavelet2.show()
        return

    def onTreeClicked(self):
        item = self.tree.currentItem()
        topCount = self.tree.topLevelItemCount()
        for i in range(0, topCount):
            if self.tree.topLevelItem(i) == item:
                self.tab.setCurrentIndex(i+1)
                if self.tree.topLevelItem(i).childCount()==0:
                    self.tree.topLevelItem(i).setSelected(1)
            if self.tree.topLevelItem(i) == item.parent():
                root = self.tree.topLevelItem(i)
                position = i
                # 子目录坐标
                ind = root.indexOfChild(item)+1
                self.tab.setCurrentIndex(position + 1)
                mdiarea = self.tab.widget(position + 1)
                list = mdiarea.subWindowList()

                list[ind].showNormal()
                list[ind].widget().show()
                mdiarea.setActiveSubWindow(list[ind])

    def onCurrentChanged(self):
        position = self.tab.currentIndex()
        if position == 0:
            return
        topCount = self.tree.topLevelItemCount()
        for i in range(0, topCount):
            if i == position - 1:
                self.tree.topLevelItem(i).setSelected(1)
            else:
                self.tree.topLevelItem(i).setSelected(0)

    def ED_A(self):
        eda = ED_ACalculation(self)
        eda.show()
        return

    def AS(self):
        asc = AS_Calculation(self)
        asc.show()
        return

    def TILT(self):
        tilt = TILT_Calculation(self)
        tilt.show()
        return

    def Theta(self):
        theta = Theta_Calculation(self)
        theta.show()
        return

    def EDT(self):
        edt = EDT_Calculation(self)
        edt.show()
        return

    def NEDT(self):
        nedt = NEDT_Calculation(self)
        nedt.show()
        return

    def EEDT(self):
        eedt = EEDT_Calculation(self)
        eedt.show()
        return

    def RRR(self):
        rrr = RRR_Calculation(self)
        rrr.show()
        return

    def NEEDT(self):
        needt = NEEDT_Calculation(self)
        needt.show()
        return

    def EAS(self):
        eas = EAS_Calculation(self)
        eas.show()

    def THDR(self):
        thdr = THDR_Calculation(self)
        thdr.show()
        return

    def Euler(self):
        euler = Euler_Calculation(self)
        euler.show()
        return

    def Filter(self):
        filter = Filter_Calculation(self)
        filter.show()
        return

    def Front_P(self):
        front_p = Front_Calculation(self)
        front_p.show()
        return

    def Left_P(self):
        left_p = Left_Calculation(self)
        left_p.show()
        return

    def Right_P(self):
        right_p = Right_Calculation(self)
        right_p.show()
        return

    def Dexp(self):
        dexp = DEXP_Calculation(self)
        dexp.show()
        return

if __name__ == "__main__":
    app = QApplication(sys.argv)
    translator = QTranslator()
    translator.load('./qt_zh_CN.qm')
    app.installTranslator(translator)
    app.setWindowIcon(QIcon("./images/Mainwindow.title.jpg"))
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())
