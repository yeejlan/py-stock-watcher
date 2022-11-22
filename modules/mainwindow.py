
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

from modules import stocklist
from modules import chartdlg

import sys

import setting

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup | Qt.WindowType.Tool)  #Qt.WindowStaysOnTopHint

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

        self.w = int(int(setting.config['window']['width'])*setting.scale)
        self.h = int(int(setting.config['window']['height'])*setting.scale)

        self.setMinimumSize(self.w, self.h)

        rect = QGuiApplication.primaryScreen().size()
        left = rect.width() - self.w
        top = rect.height() - self.h - 40
        self.move(int(left), int(top))
        self.addTrayIcon()

    def quit(self):
        self.trayIcon.setVisible(False)
        self.close()
        sys.exit()
    
    def hide(self):
        self.chartdlg.setVisible(False)
        self.setVisible(False)

    def active(self):
        self.setVisible(True)
        self.activateWindow()        

    def about(self):
        QMessageBox.about(self, 'About Stock Watcher',
            "通过Sina获取股票实时行情的小程序.\r\nEnjoy it:)")        

    def createContextMenu(self):
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
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


    def addTrayIcon(self):
        self.icon = QIcon('./images/console.png')
         
        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setIcon(self.icon)
        self.trayIcon.setToolTip("stock watcher")

        self.trayIcon.activated.connect(self.onTrayIconActivated)
       
        menu = QMenu(self)
        actionAbout = menu.addAction('关于')
        actionAbout.triggered.connect(self.about)  

        actionQuit = menu.addAction('退出')
        actionQuit.triggered.connect(self.quit)

        self.trayIcon.setContextMenu(menu) 

        self.trayIcon.show()

    def onTrayIconActivated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.active()