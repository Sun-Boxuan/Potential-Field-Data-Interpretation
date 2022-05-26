from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class DataTableWidget(QTableWidget):
    SIGNAL_data=pyqtSignal()
    def __init__(self, parent, dataset):
        super(DataTableWidget, self).__init__(parent)
        self.father = parent
# 读取文件数据
        self.dataout =dataset
        self.data = dataset
# 测线
# 设置flag判断data数组是否需要改变
        changeDataFlag = 0
        aa = []
        for i in range(0, len(self.data)):
            if self.data[i][8] not in aa:
                aa.append(self.data[i][8])
        self.lineNumber = len(aa)
        self.ny = len(aa)
# 根据xy列以及测线数量调整data
        for i in range(1, int(len(self.data) / len(aa))):
            if self.data[i][8] != self.data[0][8]:
                changeDataFlag = 1
# data需要改变
        self.dataTemp = []
        if changeDataFlag == 1:
            for j in range(0, len(aa)):
                for i in range(0, len(self.data)):
                    if aa[j] == self.data[i][8]:
                        self.dataTemp.append(self.data[i])
# 清空data
            self.data.clear()
# 赋值给data
            for i in range(0, len(self.dataTemp)):
                self.data.append(self.dataTemp[i])
            self.dataTemp.clear()
# 设置下拉列表框
        self.cb = QComboBox(self)
        cbItems = []
        for i in range(1, len(aa) + 1):
            cbItems.append('第' + str(i) + '条测线')
        self.cb.addItems(cbItems)
# 设置表格
        self.hangCount = len(self.data)//self.lineNumber
        self.lieCount = len(self.data[0])
        self.setColumnCount(9)  # 设置列数
        self.setRowCount(self.hangCount)  # 设置行数
        self.horizontalHeader().setVisible(1)
        self.verticalHeader().setVisible(1)
        self.setGeometry(0, 0, 550, 550)
        self.page = 0
# 设置表头
        self.setHorizontalHeaderLabels(['Vxx', 'Vxy', 'Vxz', 'Vyy', 'Vyz', 'Vzz', 'Vz', 'x', 'y'])
        for i in range(1, self.hangCount + 1):
            self.setItem(i, 0, QTableWidgetItem(str(i)))
        self.setColumnWidth(-1, 15)
# 设置初始化的数据
        for i in range(0, self.hangCount):
            for j in range(9):
                self.setItem(i, j, QTableWidgetItem(str(self.data[i][j])))
# 平分长度
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.showMaximized()
# 右键事件
        self.rightKeyMenu = QMenu()
        self.actionCopy = QAction("复制", self)
        self.actionCopy.setShortcut("Ctrl+C")
        self.actionCut = QAction("剪切", self)
        self.actionCut.setShortcut("Ctrl+X")
        self.actionDelete = QAction("删除", self)
        self.actionDelete.setShortcut(QKeySequence.Delete)
        self.actionPaste = QAction("粘贴", self)
        self.actionPaste.setShortcut("Ctrl+V")
# 信号槽
        self.cb.currentIndexChanged.connect(self.lineChanged)
        self.actionCopy.triggered.connect(self.onActionCopy)
        self.actionCut.triggered.connect(self.onActionCut)
        self.actionDelete.triggered.connect(self.onActionDelete)
        self.actionPaste.triggered.connect(self.onActionPaste)
# 切换测线
    def lineChanged(self):
        lineNo = self.cb.currentIndex()
#保存数据到原数组
        for i in range(0, self.hangCount):
            for j in range(0, 9):
                self.data[self.page*self.hangCount+i][j] = self.item(i, j).text()
# 展示新的数据
        self.page = lineNo
        for i in range(0, self.hangCount):
            for j in range(0, 9):
                self.setItem(i, j, QTableWidgetItem(str(self.data[lineNo * self.hangCount + i][j])))
#发射信号
        self.SIGNAL_data.emit()
# 复制
    def onActionCopy(self):
        stringCopy = ""
        selectList = self.selectedItems()
        for i in range(0, len(selectList)):
            stringCopy = stringCopy + selectList[i].text() + ","
        stringCopy += selectList[len(selectList)].text()
        board = QApplication.clipboard()
        board.setText(stringCopy)
# 剪切
    def onActionCut(self):
        stringCopy = ""
        selectList = self.selectedItems()
        for i in range(0, len(selectList)):
            stringCopy = stringCopy + selectList[i].text() + ","
            selectList[i].setText("")
        stringCopy += selectList[len(selectList)].text()
        selectList[len(selectList)].setText("")
        board = QApplication.clipboard()
        board.setText(stringCopy)
# 删除
    def onActionDelete(self):
        selectList = self.selectedItems()
        for i in range(0, len(selectList)):
            selectList[i].setText("")
# 粘贴
    def onActionPaste(self):
        board = QApplication.clipboard()
        stringPaste = board.text()
        selectList = self.selectedItems()
        stringPasteList = stringPaste.split(',')
        for i in range(0, min(len(stringPasteList), len(selectList))):
            selectList[i].setText(stringPasteList[i])
# 右键事件
    def contextMenuEvent(self, event):
        self.rightKeyMenu.clear()
# 得到窗口坐标
        point = event.pos()
        item = self.itemAt(point)
        if item != None:
            self.rightKeyMenu.addAction(self.actionCopy)
            self.rightKeyMenu.addAction(self.actionCut)
            self.rightKeyMenu.addAction(self.actionDelete)
            self.rightKeyMenu.addAction(self.actionPaste)
            self.rightKeyMenu.addSeparator()
# 菜单出现的位置为当前鼠标的位置
            self.rightKeyMenu.exec(QCursor.pos())
            event.accept()

