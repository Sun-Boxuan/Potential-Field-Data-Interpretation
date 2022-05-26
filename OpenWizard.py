from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from readtxt import read_txt
from TableWidget import DataTableWidget

class OpenWizard(QWizard):
    def __init__(self, parent):
        super(OpenWizard, self).__init__(parent)
        self.setWindowTitle("读取文件")
        self.setWindowIcon(QIcon("./images/open.jpg"))
        self.setGeometry(600, 250, 950, 350)
        self.father = parent
# 第一页
        firstPage = QWizardPage()
        firstPage.setPixmap(QWizard.WatermarkPixmap, QPixmap('./images/information.jpg'))
        label = QLabel()
        label.setText("\n\n\n\n\n\n欢迎使用")
        label.setAlignment(Qt.AlignCenter)
        layout1 = QVBoxLayout()
        layout1.addWidget(label)
        firstPage.setLayout(layout1)
# 第二页
        secondPage = QWizardPage()
        secondPage.setSubTitle('选择文件')
        self.lineEdit = QLineEdit()
        self.button = QPushButton('文件路径', secondPage)
        layout = QHBoxLayout()
        layout.addWidget(self.lineEdit, 5)
        layout.addWidget(self.button, 2)
        layout2 = QVBoxLayout()
        layout2.addStretch(5)
        layout2.addLayout(layout)
        layout2.addStretch(5)
        layout2.setAlignment(layout, Qt.AlignCenter)
        secondPage.setLayout(layout2)
# 第三页
        thirdPage = QWizardPage()
        thirdPage.setSubTitle("预览")

        self.te = QTextEdit()
        self.text2 = QLabel("项目名称:")
        self.le1 = QLineEdit()

        layout31 = QHBoxLayout()
        layout31.addStretch(1)
        layout31.addWidget(self.text2, 1)
        layout31.addWidget(self.le1, 2)
        layout31.addStretch(1)  # 界面占比

        layout3 = QVBoxLayout()
        layout3.addWidget(self.te, 4)
        layout3.addLayout(layout31, 1)
        thirdPage.setLayout(layout3)

# 数据传递变量
        self.setWizardStyle(QWizard.ModernStyle)
        self.setPage(1, firstPage)
        self.setPage(2, secondPage)
        self.setPage(3, thirdPage)
        self.setStartId(1)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)  # 设置没有帮助按钮
# 信号槽
        self.button.clicked.connect(self.chooseFile)
        self.currentIdChanged.connect(self.on_currentIdChanged)
        self.finished.connect(self.on_finished)

    def chooseFile(self):
        name = QFileDialog.getOpenFileName(self, '读取文件', './', '*.txt')
        self.lineEdit.setText(str(name[0]))
#提醒
    def validateCurrentPage(self):
        fileName = self.lineEdit.text()
        id = self.currentId()
        if id == 2 and fileName == "":
            QMessageBox.information(self, "注意", "请选择文件")
            return 0
        return 1

    def on_currentIdChanged(self):
        fileName = self.lineEdit.text()
        id = self.currentId()
        if id == 3 and fileName != "":
            filename = open(fileName)
            line1s = filename.readlines()
            self.uplimit = len(line1s)
            aa = ""
            count = 1
            for line in line1s:
                aa = aa + str(count) + "  " + line + "\n"
                count += 1
            td = QTextDocument(aa)
            self.te.setDocument(td)
            self.le1.setText(fileName.split('/')[-1])

    def on_finished(self):
# cancel键
        if self.currentId() == -1:
            return
# 获取文件名
        fileName = self.lineEdit.text()
        dataset = read_txt(fileName)

#增加子窗口
        self.father.tableWidget = DataTableWidget(self.father, dataset)
        sub = QMdiSubWindow()
        sub.resize(1250, 750)
        sub.setWidget(self.father.tableWidget)
        mdiAreaForTab = QMdiArea(self.father)
        mdiAreaForTab.addSubWindow(sub)
        self.father.tab.addTab(mdiAreaForTab, fileName.split('/')[-1])
        self.father.tab.setCurrentWidget(mdiAreaForTab)
#加根节点
        root = QTreeWidgetItem(self.father.tree)
        root.setText(0, fileName.split('/')[-1])
        sub.show()
        return
