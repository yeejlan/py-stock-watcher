
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

from modules import stocklist
from modules import chartdlg

import setting

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)

        self.setWindowTitle('Stock Watcher')
        self.setWindowIcon(QIcon('./images/console.png'))  

        self.chartdlg = chartdlg.ChartDlg(self)

        #calculate rows and cols 
        rows = len(dict(setting.config.items('hq')))
        cols = len(dict(setting.config.items('info')))
        self.stocklist = stocklist.Stocklist(rows, cols)

        w = QWidget()
        vbox = QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.addWidget(self.stocklist)
        w.setLayout(vbox)
        self.setCentralWidget(w)

        self.createContextMenu()

        self.w = int(setting.config['window']['width'])
        self.h = int(setting.config['window']['height'])

        self.setMinimumSize(self.w, self.h)

        desktop = QApplication.desktop()
        self.move(int(setting.config['window']['left']), int(setting.config['window']['top']))

    def quit(self):
        self.close()

    def about(self):
        QMessageBox.about(self, 'About Stock Watcher',
            "通过Sina获取股票实时行情的小程序.\r\nEnjoy it:)")        

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        self.contextMenu = QMenu(self)
        self.actionAbout = self.contextMenu.addAction('关于')
        self.actionQuit = self.contextMenu.addAction('退出')
        self.actionAbout.triggered.connect(self.about)
        self.actionQuit.triggered.connect(self.quit)

    def showContextMenu(self, pos):  
        self.contextMenu.move(self.pos() + pos)
        self.contextMenu.show()     

    def showChartDlg(self, code):
        self.chartdlg.updateChart(code)
        self.chartdlg.show()               

