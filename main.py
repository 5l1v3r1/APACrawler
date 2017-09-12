'''

APACrawler is a Python 3 Flask web application to automatically crawl a website and cite it in APA 6 style. More styles may be added in the future.
Copyright (C) 2017  Haoxi Tan

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>

'''


from flask import Flask,request
from bs4 import BeautifulSoup
import datetime
import urllib
import html


app = Flask(__name__) #initiates Flask app


#default page
page = open("templates/default.html","r").read()


@app.route('/') #route is the 'directory'
def main():
    #returns that page
    return page


@app.route('/cite', methods=['GET'])
def APA():
    error = None
    response = page #this will be returned to the web page
    if request.method == 'GET':

        url=request.args.get('url')
        
        #parse validity of url
        url=parse_url(url)
        print(url)

        #get the content of the URL
        try:
            source = urllib.request.urlopen(url)
        except urllib.error.URLError:
            return response + "Cannot find URL specified."


        #start parsing it with BeautifulSoup
        soup = BeautifulSoup(source, 'html.parser')
        #find all instances of <meta> (for metadata) in the soup
        meta = soup.find_all("meta")

        #find all big headings <h1> in the soup
        #h1 = soup.find_all("h1")

        #find the title
        title = soup.title.string
        print('[TITLE]')
        for i in soup.findAll('meta',{'property':True}):
            if "og:title" in i['property']:
                print(i['content'])

        title = "<br><b>Title:</b><br>" + str(title)

        meta_results = ''

        #loop over result and adds to it the response
        for i in meta:
            meta_results+=html.escape(str(i))+"<br>"
        meta_results = "<b>Metadata:</b><br>" + meta_results


        #find author
        print("[AUTHOR]")
        author = 'Not Found'
        for i in soup.findAll('meta',{'name':True}):
            if 'author' in i['name']:
                print(i['content'])
                author = i['content']
        author = "<br><br><b>Authors: </b><br>" + author


        #find h1 and h2
        h1 = ''
        print('h1:',soup.h1)
        if soup.h1 != None:
            h1 =  "<br><br><b>h1: </b><br>" + str(soup.h1.string)



        response += "results for <a href=\"%s\">%s</a>:<br><br>"%(url,url) +  meta_results + title + h1 + author


        return response


    else:
        return response

def parse_url(url):

    if url.startswith("http://")==0 and url.startswith("https://")==0:
        url="http://"+url

    print("[PARSED URL]:",url)
    return url




if __name__ == '__main__':
    app.run()
