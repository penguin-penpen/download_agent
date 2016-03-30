# -*- coding: utf-8 -*-
# 根据archieve页面逐项抓取
# key
# soup.find_all(tag, attr)

import urllib2
import pdfkit
from bs4 import BeautifulSoup
import time
import threading
# from my_thread import myThread

timing = time.clock()

# start = 12635
# end = 14210
err_html = BeautifulSoup(urllib2.urlopen('https://community.topcoder.com/stat?c=problem_statement&pm=12502').read()).find_all('td', class_='problemText')
domain = 'https://community.topcoder.com/stat?c=problem_statement&pm='
# pro_num is between 12500 to 14210
# pro_num = 12500
# -----------------------------
# 单线程
# -----------------------------
# for pro_num in range(start, end + 1):
#     url = domain + str(pro_num)
#     html = BeautifulSoup(urllib2.urlopen(url).read()).find_all('td', class_='problemText')
#     if html == err_html:
#         continue
#     path = './problems/' + str(pro_num) + '.html'
#
#     # write to disk
#     with open(path, 'w') as f:
#         f.write(str(html))
#
#     print str(pro_num) + 'done.'



# html = BeautifulSoup(urllib2.urlopen(url).read()).find_all('td', class_='problemText')
# html = BeautifulSoup(urllib2.urlopen(url).read())
# path = './problems/' + str(12500) + '.py'

# write to disk
# with open(path, 'w') as f:
#     f.write(str(html))
# path_wkthmltopdf = r'/usr/local/bin/wkhtmltopdf'
# config = pdfkit.configuration(wkhtmltopdf=path_wkthmltopdf)
# domain = 'https://community.topcoder.com/stat?c=problem_statement&pm='
# url = domain + str(12500)
# pdfkit.from_url(url, '12500.pdf')
# print str(12500) + 'done.'
#
# from cStringIO import StringIO
#
# import xhtml2pdf.pisa as pisa
#
# url = 'https://community.topcoder.com/stat?c=problem_statement&pm=12500'
# html = urllib2.urlopen(url).read()
# pdf = pisa.CreatePDF(open('html.html','rb'),open('test.pdf','wb'))
#
# if not pdf.err:
#     print "pdf is build"


# -----------------------------
# 多线程
# -----------------------------
# 引入互斥锁

class myThread(threading.Thread):
    def __init__(self, threadID, name, counter, st, end):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.st = st
        self.end = end
    def run(self):
        for pro_num in range(self.st, self.end + 1):
            url = domain + str(pro_num)
            html = BeautifulSoup(urllib2.urlopen(url).read()).find_all('td', class_='problemText')
            if html == err_html:
                continue
            path = './problems/' + str(pro_num) + '.html'

            # write to disk
            with open(path, 'w') as f:
                f.write(str(html))

            print str(pro_num) + 'done. From ' + self.name

threadLock = threading.Lock()
threads = []

# 创建新线程
thread1 = myThread(1, "Thread-1", 1, 13500, 13600)
thread2 = myThread(2, "Thread-2", 2, 13601, 13800)
thread3 = myThread(3, "Thread-3", 3, 13801, 14000)
thread4 = myThread(4, "Thread-4", 4, 14001, 14100)
thread5 = myThread(5, "Thread-5", 5, 14101, 14210)

# 开启新线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)
threads.append(thread5)

# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"

elapsed = (time.clock() - timing)
print("Time used:",(elapsed / 60))