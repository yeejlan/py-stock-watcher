
import datetime
import random
import re
import struct
import time

from modules import utils

def getStockHq(code_list):
    hqData = []
    url = 'http://hq.sinajs.cn/rn={}&list={}'.format(random.randint(1,1000000), code_list)
    err, u, content = utils.getWebContent(url)
    if(err):
        print("Error: get remote content: " + url + err)
        return False

    content = content.decode('gbk')
    hqList = re.findall(r'var hq_str_(.*)="(.*)";', content)
    for hq in hqList:
        code, data = hq
        dataArr = data.split(',')

        info = {}
        if(code[:2] == 'sh' or code[:2] == 'sz'):
            info = sh_sz_info(dataArr)
        elif(code[:2] == 'hk'):
            info = hk_info(dataArr)
        elif(code[:5] == 'rt_hk'):
            info = hk_info(dataArr)            
        elif(code[:6] == 'CFF_IF'):
            info = if_info(dataArr)
        elif(code[:6] == code and re.match('^[A-Z]+$',code)):
            info = forex_info(dataArr)            
        else :
            info = qihuo_info(dataArr)

        info['code'] = code
        if(code[:5] == 'rt_hk'):
            info['code'] = code[3:]

        hqData.append(info)

    return hqData


def sh_sz_info(dataArr):
    info = {}
    info['name'] = dataArr[0]
    info['open'] = float(dataArr[1])
    info['close_yesterday'] = float(dataArr[2])
    info['price'] = float(dataArr[3])

    if(info['price']==0):
        info['price'] = info['close_yesterday']  

    info['close'] = info['price']
    info['high'] = float(dataArr[4])
    info['low'] = float(dataArr[5])
    info['amount'] = float(dataArr[9])/1000    
    if info['close_yesterday'] > 0:
        info['price_change'] = info['price']-info['close_yesterday']
        info['price_change_percent'] = (info['price']-info['close_yesterday'])*100/info['close_yesterday']  

    info['time'] = dataArr[31]                

    return info       

def qihuo_info(dataArr):
    info = {}
    info['name'] = dataArr[0]
    info['open'] = float(dataArr[2])
    info['high'] = float(dataArr[3])
    info['low'] = float(dataArr[4])  
    info['close_yesterday'] = float(dataArr[10])  
    info['price'] = float(dataArr[8])
    if(info['price']==0):
        info['price'] = info['close_yesterday']   

    info['amount'] = float(dataArr[14])/1000

    if info['close_yesterday'] > 0:
        info['price_change'] = info['price']-info['close_yesterday']
        info['price_change_percent'] = (info['price']-info['close_yesterday'])*100/info['close_yesterday'] 

    info['time'] = '-'    

    return info

def hk_info(dataArr):
    info = {}
    info['name'] = dataArr[1]
    info['open'] = float(dataArr[2])
    info['close_yesterday'] = float(dataArr[3])
    info['price'] = float(dataArr[6])
    if(info['price']==0):
        info['price'] = info['close_yesterday']      

    info['close'] = info['price']
    info['high'] = float(dataArr[4])
    info['low'] = float(dataArr[5]) 
    if info['close_yesterday'] > 0:
        info['price_change'] = info['price']-info['close_yesterday']
        info['price_change_percent'] = (info['price']-info['close_yesterday'])*100/info['close_yesterday']  

    info['time'] = dataArr[18]     

    return info

#期指信息
def if_info(dataArr):
    info = {}
    return info

#外汇信息
def forex_info(dataArr):
    info = {}
    info['name'] = dataArr[9]
    info['open'] = float(dataArr[5])
    info['close_yesterday'] = float(dataArr[5])
    info['price'] = float(dataArr[1])
    if(info['price']==0):
        info['price'] = info['close_yesterday']   

    info['close'] = info['price']
    info['high'] = float(dataArr[6])
    info['low'] = float(dataArr[7]) 
    if info['close_yesterday'] > 0:
        info['price_change'] = info['price']-info['close_yesterday']
        info['price_change_percent'] = (info['price']-info['close_yesterday'])*100/info['close_yesterday']  

    info['time'] = dataArr[0]  
    return info


def getStockChartUrl(code):
    if(code[:2] == 'sh' or code[:2] == 'sz'):
        imageUrl = 'http://image.sinajs.cn/newchart/min/n/{}.gif?{}'.format(code, random.randint(1,1000000))
    elif(code[:2] == 'hk'):
        imageUrl = 'http://image.sinajs.cn/newchart/v5/hk_stock/min/{}.gif?{}'.format(code[2:], random.randint(1,1000000))
    elif(code[:5] == 'rt_hk'):
        imageUrl = 'http://image.sinajs.cn/newchart/v5/hk_stock/min/{}.gif?{}'.format(code[5:], random.randint(1,1000000))        
    elif(code[:6] == code and re.match('^[A-Z]+$',code)):
        imageUrl = 'http://image.sinajs.cn/newchart/v5/forex/min/{}.gif?{}'.format(code, random.randint(1,1000000))
    else:
        imageUrl = 'http://image.sinajs.cn/newchart/v5/futures/min/{}.gif?{}'.format(code, random.randint(1,1000000))

    return imageUrl