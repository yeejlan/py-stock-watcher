import configparser
import sys
import codecs
import platform
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import setting

from modules import mainwindow

config = configparser.ConfigParser()    
config.optionxform=str
with codecs.open('config.ini', 'r', 'utf8') as f:
    config.read_string(f.read())
setting.config = config

app = QApplication(sys.argv)

screen = QApplication.screens()[0]
setting.scale = (screen.logicalDotsPerInch()/96)

#main window
setting.mainwin = mainwin = mainwindow.MainWindow()
mainwin.show()


#global hotkey register
if(platform.system() == 'Windows'):	
	from modules import hotkey

	if(hotkey.registerHotkey()):
		win_event_filter = hotkey.WinEventFilter()
		app.installNativeEventFilter(win_event_filter)

sys.exit(app.exec_())