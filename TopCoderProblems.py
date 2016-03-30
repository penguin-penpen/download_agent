# -*- coding: utf-8 -*-
# 根据archieve页面逐项抓取
# key
# soup.find_all(tag, attr)

import urllib2
import pdfkit
from bs4 import BeautifulSoup
import time

timing = time.clock()

start = 12635
end = 14210
err_html = BeautifulSoup(urllib2.urlopen('https://community.topcoder.com/stat?c=problem_statement&pm=12502').read()).find_all('td', class_='problemText')
domain = 'https://community.topcoder.com/stat?c=problem_statement&pm='
# pro_num is between 12500 to 14210
# pro_num = 12500
for pro_num in range(start, end + 1):
    url = domain + str(pro_num)
    html = BeautifulSoup(urllib2.urlopen(url).read()).find_all('td', class_='problemText')
    if html == err_html:
        continue
    path = './problems/' + str(pro_num) + '.html'

    # write to disk
    with open(path, 'w') as f:
        f.write(str(html))

    print str(pro_num) + 'done.'

elapsed = (time.clock() - timing)
print("Time used:",(elapsed / 60))

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
