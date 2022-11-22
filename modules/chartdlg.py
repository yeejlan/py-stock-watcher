
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtNetwork import *

from modules import stock

import setting

class ChartDlg(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowFlags(Qt.WindowType.Tool|Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.resize(int(550*setting.scale), int(300*setting.scale))
        
        self.setWindowTitle('Chart')

        self.chart = QLabel('')

        grid = QGridLayout()
        grid.setSpacing(0)
        grid.setContentsMargins(0, 0, 0, 0)

        grid.addWidget(self.chart, 0, 0)

        self.setLayout(grid)

    def updateChart(self, code):
        imageUrl = stock.getStockChartUrl(code)
        url = QUrl(imageUrl)
        m_netwManager = QNetworkAccessManager(self)
        m_netwManager.finished.connect(self.netwManagerFinished)
        request = QNetworkRequest(url)
        m_netwManager.get(request)

    def netwManagerFinished(self, reply):
        if(reply.error() != QNetworkReply.NetworkError.NoError):
            print("Error in" + reply.url() + ":" + reply.errorString())
            return False

        imgData = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(imgData)
        self.chart.setPixmap(pixmap.scaled(int(550*setting.scale), int(300*setting.scale)))