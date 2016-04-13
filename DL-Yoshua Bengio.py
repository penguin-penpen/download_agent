# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import pdfkit
import time

class simplePage:
    def __init__(self, domain, url):
        self.domain = domain
        self.url = url

    def fakeHeader(self):
        header={
            "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:43.0) Gecko/20100101 Firefox/43.0",
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Host":"baidu.com"
        }
        return header


    def getItems(self, mark = 'a', className = None):
        request = urllib2.Request(self.url, headers=self.fakeHeader())
        html = BeautifulSoup(urllib2.urlopen(request).read())
        items = html.find_all(mark, class_ = className)
        return items

    def downloadAsHTML(self):
        links = self.getItems()
        for link in links[7:]:
            joinedURL = self.domain + link.get('href')
            html = urllib2.urlopen(joinedURL).read()
            print joinedURL
            name = str(link.text) + '.html'
            try:
                with open(name, 'w') as f:
                    f.write(html)
            except urllib2.HTTPError:
                pass
            except:
                pass
            finally:
                time.sleep(5)

    def downloadAsPDF(self):
        links = self.getItems()
        for link in links:
            name = str(link.text) + '.pdf'
            joinedURL = self.domain + link.get('href')
            print joinedURL
            try:
                pdfkit.from_url(joinedURL, name)
                print 'success!'
            except:
                print 'error...'


url = 'http://www.deeplearningbook.org/'
domain = 'http://www.deeplearningbook.org/'
page = simplePage(domain, url)
page.downloadAsHTML()
