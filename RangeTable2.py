from PyQt5.QtWidgets import *

class ModelWizardWidget2(QWidget):
    def __init__(self, parent, obnum):
        super(ModelWizardWidget2, self).__init__(parent)

        obnum = int(obnum)
        self.tableWidget = QTableWidget()
        self.tableWidget.horizontalHeader().setVisible(1)
        self.tableWidget.verticalHeader().setVisible(1)
        self.tableWidget.setColumnCount(6)
        self.tableWidget.setRowCount(obnum)

        self.tableWidget.setHorizontalHeaderLabels(
            ['X轴方向 \n 起始坐标', 'X轴方向 \n 终点坐标', 'Y轴方向 \n 起始坐标', 'Y轴方向 \n 终点坐标', 'Z轴方向 \n 起始坐标', 'Z轴方向 \n 终点坐标'])
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setShowGrid(True)
        for i in range(0, obnum):
            for j in range(0, 6):
                self.tableWidget.setItem(i, j, QTableWidgetItem(''))
        layout = QVBoxLayout()
        layout.addWidget(self.tableWidget)
        self.setLayout(layout)
