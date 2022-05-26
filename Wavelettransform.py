from skimage.restoration import denoise_wavelet
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from TableWidget import DataTableWidget
#小波变换
class Wavelettransform(QWidget):
    def __init__(self, parent):
        super(Wavelettransform, self).__init__(parent)
        self.setGeometry(550, 350, 1050, 350)
        self.father = parent
        self.setWindowTitle('小波变换去噪')

# 界面
        layoutline1 = QHBoxLayout()
        self.label1 = QLabel('小波基选择：')
        self.p0 = QComboBox(self)
        self.p0.addItem('haar')
        self.p0.addItem('db2')
        self.p0.addItem('db3')
        self.p0.addItem('db4')
        self.p0.addItem('db5')
        self.p0.addItem('db6')
        self.p0.addItem('db7')
        self.p0.addItem('db8')
        self.p0.addItem('db9')
        self.p0.addItem('db10')
        self.p0.addItem('db11')
        self.p0.addItem('db12')
        self.p0.addItem('db13')
        self.p0.addItem('db14')
        self.p0.addItem('db15')
        self.p0.addItem('db16')
        self.p0.addItem('db17')
        self.p0.addItem('db18')
        self.p0.addItem('db19')
        self.p0.addItem('db20')
        self.p0.addItem('db21')
        self.p0.addItem('db22')
        self.p0.addItem('db23')
        self.p0.addItem('db24')
        self.p0.addItem('db25')
        self.p0.addItem('db26')
        self.p0.addItem('db27')
        self.p0.addItem('db28')
        self.p0.addItem('db29')
        self.p0.addItem('db30')
        self.p0.addItem('db31')
        self.p0.addItem('db32')
        self.p0.addItem('db33')
        self.p0.addItem('db34')
        self.p0.addItem('db35')
        self.p0.addItem('db36')
        self.p0.addItem('db37')
        self.p0.addItem('db38')

        self.p0.addItem('sym2')
        self.p0.addItem('sym3')
        self.p0.addItem('sym4')
        self.p0.addItem('sym5')
        self.p0.addItem('sym6')
        self.p0.addItem('sym7')
        self.p0.addItem('sym8')
        self.p0.addItem('sym9')
        self.p0.addItem('sym10')
        self.p0.addItem('sym11')
        self.p0.addItem('sym12')
        self.p0.addItem('sym13')
        self.p0.addItem('sym14')
        self.p0.addItem('sym15')
        self.p0.addItem('sym16')
        self.p0.addItem('sym17')
        self.p0.addItem('sym18')
        self.p0.addItem('sym19')
        self.p0.addItem('sym20')

        self.p0.addItem('coif1')
        self.p0.addItem('coif2')
        self.p0.addItem('coif3')
        self.p0.addItem('coif4')
        self.p0.addItem('coif5')
        self.p0.addItem('coif6')
        self.p0.addItem('coif7')
        self.p0.addItem('coif8')
        self.p0.addItem('coif9')
        self.p0.addItem('coif10')
        self.p0.addItem('coif11')
        self.p0.addItem('coif12')
        self.p0.addItem('coif13')
        self.p0.addItem('coif14')
        self.p0.addItem('coif15')
        self.p0.addItem('coif16')
        self.p0.addItem('coif17')

        self.p0.addItem('gaus1')
        self.p0.addItem('gaus2')
        self.p0.addItem('gaus3')
        self.p0.addItem('gaus4')
        self.p0.addItem('gaus5')
        self.p0.addItem('gaus6')
        self.p0.addItem('gaus7')
        self.p0.addItem('gaus8')

        self.p0.addItem('cgau1')
        self.p0.addItem('cgau2')
        self.p0.addItem('cgau3')
        self.p0.addItem('cgau4')
        self.p0.addItem('cgau5')
        self.p0.addItem('cgau6')
        self.p0.addItem('cgau7')
        self.p0.addItem('cgau8')

        self.p0.addItem('mexh')
        self.p0.addItem('demy')
        self.p0.setCurrentIndex(0)

        layoutline1.addStretch(1)
        layoutline1.addWidget(self.label1, 2)
        layoutline1.addStretch(1)
        layoutline1.addWidget(self.p0, 3)
        layoutline1.addStretch(1)

        layoutline2 = QHBoxLayout()
        self.label2 = QLabel('分解层数：')
        self.fen = QLineEdit()
        self.fen.setText('3')

        layoutline2.addStretch(1)
        layoutline2.addWidget(self.label2, 2)
        layoutline2.addStretch(1)
        layoutline2.addWidget(self.fen, 3)
        layoutline2.addStretch(1)

        layoutline3 = QHBoxLayout()
        self.label3 = QLabel('阈值：')
        self.yu = QComboBox(self)
        self.yu.addItem('软')
        self.yu.addItem('硬')
        self.yu.setCurrentIndex(0)

        layoutline3.addStretch(1)
        layoutline3.addWidget(self.label3, 2)
        layoutline3.addStretch(1)
        layoutline3.addWidget(self.yu, 3)
        layoutline3.addStretch(1)


        layoutline4 = QHBoxLayout()
        self.label4 = QLabel('新数据名称：')
        self.pn = QLineEdit()
        self.pn.setText('Wavelet-transform File')

        layoutline4.addStretch(1)
        layoutline4.addWidget(self.label4, 2)
        layoutline4.addStretch(1)
        layoutline4.addWidget(self.pn, 8)
        layoutline4.addStretch(1)

        layoutline5 = QHBoxLayout()
        self.button1 = QPushButton('计算')
        self.button2 = QPushButton('取消')
        layoutline5.addWidget(self.button1)
        layoutline5.addWidget(self.button2)

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

        layout2 = QVBoxLayout()
        self.label21 = QLabel()
        self.label21.setPixmap(QPixmap('./images/Drawing07.png'))
        layout2.addWidget(self.label21, 1)

        layout = QHBoxLayout()
        layout.addLayout(layout2, 1)
        layout.addLayout(layout1, 2)
        self.setLayout(layout)
        self.setWindowFlags(Qt.Dialog | Qt.WindowCloseButtonHint)
# 信号槽
        self.button1.clicked.connect(self.on_ok_clicked)
        self.button2.clicked.connect(self.on_cancel_clicked)

    def on_cancel_clicked(self):
        self.close()
        return

    def on_ok_clicked(self):

        position = self.father.tab.currentIndex()

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
            tableWidget = self.father.tab.widget(position).subWindowList()[0].widget()
            dataset = tableWidget.dataout

            Vxx = dataset[:, 0]
            Vxx = Vxx.astype(float)
            Vxy = dataset[:, 1]
            Vxy = Vxy.astype(float)
            Vxz = dataset[:, 2]
            Vxz = Vxz.astype(float)
            Vyy = dataset[:, 3]
            Vyy = Vyy.astype(float)
            Vyz = dataset[:, 4]
            Vyz = Vyz.astype(float)
            Vzz = dataset[:, 5]
            Vzz = Vzz.astype(float)
            Vz = dataset[:, 6]
            Vz = Vz.astype(float)

            x = dataset[:, 7]
            y = dataset[:, 8]
            len_x = len(np.unique(x))
            len_y = len(np.unique(y))

            Vxx = Vxx.reshape(len_x, len_y)
            Vxy = Vxy.reshape(len_x, len_y)
            Vxz = Vxz.reshape(len_x, len_y)
            Vyy = Vyy.reshape(len_x, len_y)
            Vyz = Vyz.reshape(len_x, len_y)
            Vzz = Vzz.reshape(len_x, len_y)
            Vz = Vz.reshape(len_x, len_y)
            x = x.reshape(len_x, len_y)
            y = y.reshape(len_x, len_y)
            dbx = self.p0.currentText()
            mode1 = self.yu.currentIndex()
            if mode1 == 0:
                mode2 = 'soft'
            else:
                mode2 = 'hard'
            level2 = self.fen.text()
            fileName = self.pn.text()

            im_haar_Vxx = denoise_wavelet(Vxx, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)
            im_haar_Vxy = denoise_wavelet(Vxy, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)
            im_haar_Vxz = denoise_wavelet(Vxz, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)
            im_haar_Vyy = denoise_wavelet(Vyy, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)
            im_haar_Vyz = denoise_wavelet(Vyz, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)
            im_haar_Vzz = denoise_wavelet(Vzz, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)
            im_haar_Vz = denoise_wavelet(Vz, mode=mode2, wavelet_levels=int(level2), wavelet=str(dbx), multichannel=True)

            im_haar_Vxx = im_haar_Vxx.reshape(-1, 1)
            im_haar_Vxy = im_haar_Vxy.reshape(-1, 1)
            im_haar_Vxz = im_haar_Vxz.reshape(-1, 1)
            im_haar_Vyy = im_haar_Vyy.reshape(-1, 1)
            im_haar_Vyz = im_haar_Vyz.reshape(-1, 1)
            im_haar_Vzz = im_haar_Vzz.reshape(-1, 1)
            im_haar_Vz = im_haar_Vz.reshape(-1, 1)
            x = x.reshape(-1, 1)
            y = y.reshape(-1, 1)

            dataset_n = np.hstack((im_haar_Vxx, im_haar_Vxy, im_haar_Vxz, im_haar_Vyy, im_haar_Vyz, im_haar_Vzz, im_haar_Vz, x, y))
            dataset_n = np.array(dataset_n)

# 增加子窗口
            self.father.tableWidget = DataTableWidget(self.father, dataset_n)
            sub = QMdiSubWindow()
            sub.setWidget(self.father.tableWidget)
            mdiAreaForTab = QMdiArea(self.father)
            mdiAreaForTab.addSubWindow(sub)
            self.father.tab.addTab(mdiAreaForTab, fileName.split('/')[-1])
            self.father.tab.setCurrentWidget(mdiAreaForTab)
            sub.resize(1250, 750)

# 加根节点
            root = QTreeWidgetItem(self.father.tree)
            root.setText(0, fileName.split('/')[-1])
            sub.show()
            self.close()
            return