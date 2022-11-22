
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *

import setting

from modules import utils
from modules import stock

class Stocklist(QTableWidget):

	def __init__(self, *args):
		super().__init__(*args)

		hview = DragableHeaderView(Qt.Orientation.Horizontal)
		hview.setDefaultSectionSize(int(int(setting.config['window']['column_width'])*setting.scale))
		self.setHorizontalHeader(hview)
		vview = DragableHeaderView(Qt.Orientation.Vertical)
		vview.setDefaultSectionSize(int(int(setting.config['window']['row_height'])*setting.scale))
		self.setVerticalHeader(vview)

		self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
		self.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)

		#get stock list
		self.getStockList()
		
		#realtime hq update
		self.rt_timer = QTimer()
		self.rt_timer.setInterval(3000)
		self.rt_timer.timeout.connect(self.stockHqUpdate)
		self.rt_timer.start()

		#set header
		horHeaders = []
		infoKeys = []
		for key, value in setting.config.items('info'):
			horHeaders.append(value)
			infoKeys.append(key)
		self.setHorizontalHeaderLabels(horHeaders)
		self.infoKeys = infoKeys

		self.stockHqUpdate()

		#set selected style
		self.setStyleSheet('QTableWidget::item:selected{ background: rgba(0, 0, 150, 100); }')

		self.itemDoubleClicked.connect(self.itemDoubleClickedHandler)
		self.cellDoubleClicked.connect(self.cellDoubleClickedHandler)

	def getStockList(self):
		stockList = []
		for key in setting.config['hq']:
			code = key.strip()
			stockList.append(code)

		self.stockList = stockList


	def stockHqUpdate(self):
		hqList = stock.getStockHq(','.join(self.stockList))

		for n, hq in enumerate(hqList):
			for m, key in enumerate(self.infoKeys):
				try:
					value = hq[key]
					if(key=='code' or key=='name' or key=='time'):
						newitem = QTableWidgetItem(value)
						newitem.setForeground(Qt.GlobalColor.black)
						if(key=='time'):
							newitem.setTextAlignment(Qt.AlignmentFlag.AlignRight)
					elif(key=='price_change_percent'):
						newitem = QTableWidgetItem('{:-.2f}%'.format(value))
						newitem.setTextAlignment(Qt.AlignmentFlag.AlignRight)
						if(value>0):
							newitem.setForeground(Qt.GlobalColor.red)
						elif(value == 0):
							newitem.setForeground(Qt.GlobalColor.black)
						else:
							newitem.setForeground(Qt.GlobalColor.darkGreen)
					else:
						valStr = '{:-.3f}'.format(value)
						if(valStr[-1:] == '0'):
							valStr = valStr[:-1]
						newitem = QTableWidgetItem(valStr)	
						newitem.setTextAlignment(Qt.AlignmentFlag.AlignRight)
						if(key=='price_change'):
							if(value>0):
								newitem.setForeground(Qt.GlobalColor.red)
							elif(value == 0):
								newitem.setForeground(Qt.GlobalColor.black)
							else:
								newitem.setForeground(Qt.GlobalColor.darkGreen)		
						else:
							if(value>hq['close_yesterday']):
								newitem.setForeground(Qt.GlobalColor.red)
							elif(value == hq['close_yesterday']):
								newitem.setForeground(Qt.GlobalColor.black)
							else:
								newitem.setForeground(Qt.GlobalColor.darkGreen)														

				except KeyError:
					value = ''
					newitem = QTableWidgetItem(value)
					newitem.setForeground(Qt.GlobalColor.black)					

				newitem.setFlags(Qt.ItemFlag.ItemIsEnabled)
				self.setItem(n, m, newitem)


	def itemDoubleClickedHandler(self, event):
		select = self.selectionModel()
		if(select.hasSelection()):
			code = select.selectedRows()[0].data()
			setting.mainwin.showChartDlg(code)

	def cellDoubleClickedHandler(self, row, col):
		code = self.item(row, 0).text()
		setting.mainwin.showChartDlg(code)


class DragableHeaderView(QHeaderView):
	def __init__(self, *args):
		super().__init__(*args)

	def mousePressEvent(self, event):
		if event.button() == Qt.MouseButton.LeftButton:
			setting.mainwin.dragPosition = event.globalPosition() - QPointF(setting.mainwin.frameGeometry().topLeft())
			event.accept()

	def mouseMoveEvent(self, event):
		if event.buttons() == Qt.MouseButton.LeftButton:
			setting.mainwin.move((event.globalPosition() - setting.mainwin.dragPosition).toPoint())
			event.accept()