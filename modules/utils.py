import datetime
import imp
import os
import queue
import sys
import threading
import time
import traceback
import urllib.request
import urllib.parse

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import setting

def getWebContent(url):  #return tuple(error, url, content)

    in_queue = queue.Queue()
    in_queue.put(url)
    out_queue = queue.Queue()
    getWebContentMT(in_queue, out_queue)
    while(True):
        try:
            retval = out_queue.get(False)
            break
        except queue.Empty:
            time.sleep(0.01)
            QCoreApplication.processEvents()

    return retval

def _getWebContent(remote_url):  #internal function, return tuple(error, url, content)
    error = None
    content = ''
    try:
        req = urllib.request.Request(remote_url)
        req.add_header('Referer', remote_url)
        req.add_header('User-Agent', setting.useragent)
        res = urllib.request.urlopen(req, None, 30)
        content = res.read()
    except:
        exc_type, exc_value = sys.exc_info()[:2]
        error = '{}: {}'.format(exc_type.__name__, exc_value)
        
    return (error, remote_url, content)

'''
in_queue  item: url(String) the url we want to fetch
out_queue item: tuple(error, url, content) the web content we got
'''
def getWebContentMT(in_queue, out_queue, thread_max = 1, thread_name = ''):  #use multi-thread to get web content
    thread_list = []
    for i in range(0, thread_max):
        t = _GetWebContentWorker(in_queue, out_queue, thread_name)
        thread_list.append(t)
        t.start()
    
    return thread_list

def file_get_contents(filename, mode='r'):
    try:
        f = open(filename, mode)
    except IOError:
        exc_type, exc_value = sys.exc_info()[:2]
        errmsg = '{}: {}'.format(exc_type.__name__, exc_value)
        #output(errmsg, 'red')
        return False

    return f.read()

def md5(str, encoding = 'utf8'):
    m = hashlib.md5()
    m.update(str.encode(encoding))
    return m.hexdigest()


class _GetWebContentWorker(threading.Thread):
    def __init__(self, in_queue, out_queue, thread_name):
        threading.Thread.__init__(self)
        self.in_queue = in_queue
        self.out_queue = out_queue
        self.running = True
        if(thread_name != ''):
            self.name = thread_name

    def run(self):
        while(self.running):
            try:
                url = self.in_queue.get(False)
                self.out_queue.put(_getWebContent(url))
                self.in_queue.task_done()
            except queue.Empty:
                break
      
    def stop(self):
        self.running = False

                