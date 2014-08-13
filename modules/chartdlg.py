
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtNetwork import *

from modules import stock

class ChartDlg(QDialog):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.setWindowFlags(Qt.Tool|Qt.MSWindowsFixedSizeDialogHint)
        self.resize(550, 300)
        
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
        if(reply.error() != QNetworkReply.NoError):
            print("Error in" + reply.url() + ":" + reply.errorString())
            return False

        imgData = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(imgData)
        self.chart.setPixmap(pixmap)