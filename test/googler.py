#!/usr/bin/python3
'''
quick and dirty script to grep a bunch of URLS off google for fuzzing apacrawler

'''

from bs4 import BeautifulSoup
import urllib.request
import sys


if len(sys.argv)<2:
    print("Usage: googler.py <one keyword>")
    exit()

keyword = sys.argv[1]
url = "https://www.google.co.nz/search?q=%s" % keyword

opener = urllib.request.build_opener()
urllib.request.install_opener(opener)
#set useragent to mozilla
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]
source = opener.open(url)

soup = BeautifulSoup(source,'html.parser')
links = soup.find_all("a")

for link in links:
    if str(link['href']).startswith("/url?q="):
        print(link['href'].strip('/url?q=\'\''))