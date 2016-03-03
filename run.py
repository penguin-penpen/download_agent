# -*- coding: utf-8 -*-

import requests
import urllib2
import threading
import Queue
import urllib
import time
from bs4 import BeautifulSoup
from collections import defaultdict

# declare globals
thread_number = 6
data = []

def get_links():
    session = requests.session()
    htmls = []
    for year in range(2010,2015):
        u = str(year)
        url = 'http://cs229.stanford.edu/projects' + u + '.html'
        htmls.append(session.get(url).content)
        print 'get doc ' + u + ' successfully!'

        links = []
        for html in htmls:
            soup = BeautifulSoup(html)
            for link in soup.find_all('a'):
                links.append(link.get('href'))
                # print link
            links = links[1:]
            for link in links:
                add = str(link).replace(' ', '%20')
                link = 'http://cs229.stanford.edu/' + add
            return links


def download_from_urls(links):
    for link in links:
        add = str(link).replace(' ', '%20')
        download_link = 'http://cs229.stanford.edu/' + add
        # content = session.get(download_link).content
        r = requests.get(download_link)
        with open(str(link)[9:], 'wb') as f:
            f.write(r.content)
            # print content
    return

url = 'http://cs229.stanford.edu/proj2010/Held-4WayStopWaitTimePrediction.pdf'
# 获取头部信息
# response = urllib2.urlopen(url)
# headers = response.info()
# print headers
#
# file_len = int(headers['Content-Length'])
# download_range = file_len / 10
# left_data_range = file_len % 10
#
# start = 0
# end = download_range - 1
# request = urllib2.Request(url)
# request.headers['Range'] = 'bytes=%s-%s' % (start, end)
# data = urllib2.urlopen(request).read()


def get_headers(url):
    # 获取头部信息
    response = urllib2.urlopen(url)
    headers = response.info()
    return headers


def divide_chunks(headers):
    file_len = int(headers['Content-Length'])
    # global thread_number
    chunk_length = file_len / (thread_number - 1)
    left_chunk_length = file_len % (thread_number - 1)
    return chunk_length, left_chunk_length


def download_chunk(url, start, end):
    request = urllib2.Request(url)
    request.headers['Range'] = 'bytes=%s-%s' % (start, end)
    chunk_data = urllib2.urlopen(request).read()
    return chunk_data


def write_file(filename ,content):
    try:
        with open(filename, 'a+') as f:
            f.write(content)
    finally:
        pass
    return

# 线程类
class myThread (threading.Thread):

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    # 重写run函数
    def run(self, url, start, end):
        print "Starting " + self.name
        global data
        chunk = download_chunk(url, start, end)
        data.append(chunk)
        # 获得锁，成功获得锁定后返回True
        # 可选的timeout参数不填时将一直阻塞直到获得锁定
        # 否则超时后将返回False
        # thread_lock.acquire()
        # print_time(self.name, self.counter, 3)
        # 释放锁
        # thread_lock.release()


# timer
start_time = time.clock()
print 'start...'

links = get_links()

# for url in links:
url = 'http://cs229.stanford.edu/proj2010/Held-4WayStopWaitTimePrediction.pdf'
headers = get_headers(url)
chunk_length, left_chunk_length = divide_chunks(headers)
global thread_number
# chunk_range储存每个完整线程的首尾
chunk_range = defaultdict(list)
for i in range(thread_number - 1):
    chunk_range[i].append(i*chunk_length)
    chunk_range[i].append(i*chunk_length + (chunk_length - 1))
chunk_range[thread_number - 1].append(thread_number * chunk_length)
chunk_range[thread_number - 1].append(-1)

# start threads

threads = []

# 创建新线程
thread1 = myThread(1, 'Thread-1', 1)
thread2 = myThread(2, 'Thread-2', 2)
thread3 = myThread(3, 'Thread-3', 3)
thread4 = myThread(4, 'Thread-4', 4)
thread5 = myThread(5, 'Thread-5', 5)
thread6 = myThread(6, 'Thread-6', 6)

# 开启新线程
thread1.start()
thread2.start()
thread3.start()
thread4.start()
thread5.start()
thread6.start()

# 添加线程到线程列表
threads.append(thread1)
threads.append(thread2)
threads.append(thread3)
threads.append(thread4)
threads.append(thread5)
threads.append(thread6)

# run
for i in range(thread_number):
    threads[i].run(url, chunk_range[i][0], chunk_range[i][1])

# 等待所有线程完成
for t in threads:
    t.join()
print "Exiting Main Thread"

for i in range(0, thread_number):
    write_file(url[35:],data[i])


# 引入互斥锁
thread_lock = threading.Lock()

# download_link = 'http://cs229.stanford.edu/proj2010/Held-4WayStopWaitTimePrediction.pdf'
# # content = session.get(download_link).content
# r = requests.get(download_link)
# with open('1.pdf', 'wb') as f:
#     f.write(r.content)

elapsed = (time.clock() - start_time)
print 'time used:' + str(elapsed)






