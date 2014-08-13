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
config.readfp(codecs.open('config.ini', 'r', 'utf8'))  
setting.config = config

app = QApplication(sys.argv)

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