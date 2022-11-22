import ctypes
from ctypes import c_bool, c_int, WINFUNCTYPE, windll
from ctypes.wintypes import UINT

from PyQt6.QtCore import *

import setting

HOT_KEY_ID = 1
WM_HOTKEY = 0x0312
MOD_ALT = 0x0001
MOD_NONE = 0x000
MOD_CONTROL = 0x0002
MOD_SHIFT = 0x0004
MOD_WIN = 0x0008

class WinEventFilter(QAbstractNativeEventFilter):

	def nativeEventFilter(self, eventType, message):
		msg = ctypes.wintypes.MSG.from_address(message.__int__())
		if msg.message == WM_HOTKEY:
			if(setting.mainwin.isActiveWindow()):  #isVisible()
				setting.mainwin.hide()
			else:
				setting.mainwin.active()

			return True, 0		

		return False, 0


def registerHotkey():
	
	modifier = MOD_ALT
	if(setting.config['hotkey']['modifier'] == 'shift'):
		modifier = MOD_SHIFT
	elif(setting.config['hotkey']['modifier'] == 'ctrl'):
		modifier = MOD_CONTROL

	key = ord(setting.config['hotkey']['key'].upper())

	prototype = WINFUNCTYPE(c_bool, c_int, c_int, UINT, UINT)
	paramflags = (1, 'hWnd', 0), (1, 'id', 0), (1, 'fsModifiers', 0), (1, 'vk', 0)
	registerHotKey = prototype(('RegisterHotKey', windll.user32), paramflags)
	success = registerHotKey(c_int(int(setting.mainwin.winId())), HOT_KEY_ID, modifier, key)
	if(not success):
		print('Register global hotkey error')
		return False
	
	return True
