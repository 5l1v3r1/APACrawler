'''
tester for apacrawler, imports links from a file and cite them.

'''


from bs4 import BeautifulSoup
import urllib.request
import sys

if len(sys.argv)<2:
    print("Usage: fuzz.py <file with links>")
    exit()


#build url opener
opener = urllib.request.build_opener()
urllib.request.install_opener(opener)
#set useragent to mozilla
opener.addheaders = [('User-Agent', 'Mozilla/5.0')]


with open(sys.argv[1]) as file:
    for url in file:
        try:
            print("[URL]:",url)
            print(opener.open(url))
        except urllib.error.HTTPError as error:
            print("error:",error)
