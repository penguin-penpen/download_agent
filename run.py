# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

def download_from_url():
    session = requests.session()
    htmls = []
    for year in range(2009,2015):
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
                download_link = 'http://cs229.stanford.edu/' + add
                # content = session.get(download_link).content
                r = requests.get(download_link)
                with open(str(link)[9:], 'wb') as f:
                    f.write(r.content)
                # print content
    return

download_from_url()