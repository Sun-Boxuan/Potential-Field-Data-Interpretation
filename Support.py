import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from RangeTable2 import ModelWizardWidget2


class Support_Calculation(QWizard):
    def __init__(self, parent):
        super(Support_Calculation, self).__init__(parent)
        self.father = parent
        plt.rcParams['font.family'] = ['SimHei']  # 用来正常显示中文标签
        plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

        self.setWindowTitle('辅助功能')
        self.setWindowIcon(QIcon('./images/Mainwindow.title.jpg'))
        self.setGeometry(550, 150, 350, 350)

#第一页
        firstPage = QWizardPage()
        firstPage.setSubTitle('线框的数量')
        firstPage.setPixmap(QWizard.WatermarkPixmap, QPixmap('./record/pic.png'))
        layoutline0 = QHBoxLayout()
        self.label0 = QLabel('请输入辅助线框的数量:')
        self.obnum = QLineEdit()
        self.obnum.setValidator(QIntValidator())
        self.obnum.setText('1')

        layoutline0.addWidget(self.label0, 1)
        layoutline0.addWidget(self.obnum, 1)

        firstPage.setLayout(layoutline0)
        firstPage.setCommitPage(1)
#第二页
        secondPage = QWizardPage()
        secondPage.setSubTitle('请输入辅助线框的坐标范围')
        secondPage.setPixmap(QWizard.WatermarkPixmap, QPixmap('./images/Drawing08.png'))
        obnum = int(self.obnum.text())
        self.inputTable = ModelWizardWidget2(self, obnum)
        self.layout2 = QVBoxLayout()
        self.checkbox = QCheckBox('模型中显示辅助线框')
        self.checkbox.setChecked(False)

        self.layout2.addWidget(self.inputTable, 6)
        self.layout2.addWidget(self.checkbox, 2)

        secondPage.setLayout(self.layout2)

        self.setWizardStyle(QWizard.ModernStyle)
        self.setPage(1, firstPage)
        self.setPage(2, secondPage)
        self.setStartId(1)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)

# 信号槽
        self.currentIdChanged.connect(self.on_currentIdChanged)
        self.finished.connect(self.on_finish_clicked)
        self.checkbox.stateChanged.connect(self.support1)

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
                for i in range(0, 6):
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
        return 1

    def on_currentIdChanged(self):
        id = self.currentId()
        if id == 2:
            obnum = int(self.obnum.text())
            self.obnum2 = obnum
            self.inputTable.tableWidget.setRowCount(obnum)
            return

    def support1(self):
        if self.checkbox.isChecked():
            self.father.signal2 = 1
        else:
            self.father.signal2 = 0


    def on_finish_clicked(self):
        if self.currentId() == -1:
            self.father.signal2 = 0
            return
        rowcount = int(self.obnum.text())
        dataset_temp = []
        for j in range(0, rowcount):
            for i in range(0, 6):
                data2 = self.inputTable.tableWidget.item(j, i).text()
                dataset_temp.append(data2)

        dataset1 = np.array(dataset_temp, dtype=float)
        self.dataset1 = dataset1.reshape(rowcount, 6)
        np.savetxt("./record/range2.txt", self.dataset1)
        rowcount1 = str(rowcount)
        with open('./record/rowcount.txt', 'w') as f:
            f.write(rowcount1)
        return

