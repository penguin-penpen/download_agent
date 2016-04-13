# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import pdfkit
import time

class simplePage:
    def __init__(self, domain, url):
        self.domain = domain
        self.url = url


    def getItems(self, mark = 'a', className = None):
        html = BeautifulSoup(urllib2.urlopen(self.url).read())
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
