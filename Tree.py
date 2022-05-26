from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class TreeWidget(QTreeWidget):
    def __init__(self, parent):
        super(TreeWidget, self).__init__(parent)
        self.father = parent
        # 右键事件
        self.rightKeyMenu = QMenu()
        self.actionSave = QAction("保存", self)
        self.actionDelete = QAction("删除", self)
        self.actionExpand = QAction("展开", self)
        self.actionZhe = QAction("折叠", self)
        # 信号槽
        self.actionSave.triggered.connect(self.on_Save)
        self.actionDelete.triggered.connect(self.on_Delete)
        self.actionExpand.triggered.connect(self.on_Expand)
        self.actionZhe.triggered.connect(self.on_Zhe)
    # 保存操作
    def on_Save(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList) != 1:
            return
        item = selectedList[0]
        root = item.parent()
        ind = root.indexOfChild(item)
        mw = self.father.tab.currentWidget().subWindowList()[ind].widget()
        name = QFileDialog.getSaveFileName(self, '打开文件', './', '*.png *.pdf *.jpg')
        mw.mpl.saveFig(name[0])
    # 删除操作
    def on_Delete(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList) != 1:
            return
        item = selectedList[0]
        root = item.parent()
        ind = root.indexOfChild(item)
        root.takeChild(ind)
        mdiarea = self.father.tab.currentWidget()
        mdiarea.removeSubWindow(mdiarea.subWindowList()[ind])
    # 展开操作
    def on_Expand(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList) != 1:
            return
        item = selectedList[0]
        item.setExpanded(1)
    # 折叠操作
    def on_Zhe(self):
        selectedList = self.father.tree.selectedItems()
        if len(selectedList) != 1:
            return
        item = selectedList[0]
        item.setExpanded(0)
    # 右键事件
    def contextMenuEvent(self, event):

        self.rightKeyMenu.clear()
    # 得到窗口坐标
        point = event.pos()
        item = self.itemAt(point)
        if item == None:
            return
        topCount = self.father.tree.topLevelItemCount()
        for i in range(0, topCount):
            if self.father.tree.topLevelItem(i) == item:
                if item.isExpanded() == 0:
                    self.rightKeyMenu.addAction(self.actionExpand)
                else:
                    self.rightKeyMenu.addAction(self.actionZhe)

            if self.father.tree.topLevelItem(i) == item.parent():
                # 如果是第一个孩子，则没有右键目录
                index = item.parent().indexOfChild(item)
                if index == 0:
                    return
                if item.text(0) == "3D Model":
                    self.rightKeyMenu.addAction(self.actionSave)
                else:
                    self.rightKeyMenu.addAction(self.actionSave)
                    self.rightKeyMenu.addAction(self.actionDelete)
            # 菜单出现的位置为当前鼠标的位置
        self.rightKeyMenu.exec(QCursor.pos())
        event.accept()
