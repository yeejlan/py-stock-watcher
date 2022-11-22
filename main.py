import configparser
import sys
import codecs
import platform
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *

import setting

from modules import mainwindow

config = configparser.ConfigParser()    
config.optionxform=str
with codecs.open('config.ini', 'r', 'utf8') as f:
    config.read_string(f.read())
setting.config = config

app = QApplication(sys.argv)
font = app.font();
window_config = dict(setting.config.items('window'))
font.setPixelSize(int(window_config['font_size']));
app.setFont(font);

#main window
setting.mainwin = mainwin = mainwindow.MainWindow()
mainwin.show()


#global hotkey register
if(platform.system() == 'Windows'):	
	from modules import hotkey

	if(hotkey.registerHotkey()):
		win_event_filter = hotkey.WinEventFilter()
		app.installNativeEventFilter(win_event_filter)

sys.exit(app.exec())