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


from flask import Flask,request,render_template
from bs4 import BeautifulSoup
import datetime
import urllib
import html


app = Flask(__name__) #initiates Flask app


@app.route('/') #route is the 'directory'
def main():
    return render_template("index.html")


@app.route('/cite', methods=['GET'])
def cite():
    error = None
    response = '' #this will be the server's response to add to the template
    if request.method == 'GET':

        url=request.args.get('url')
        
        #parse validity of url
        url=parse_url(url)
        print(url)

        #get the content of the URL
        try:
            source = urllib.request.urlopen(url)
        except urllib.error.URLError:
            return render_template("index.html") + "Cannot find URL specified."


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

        title_debug = "<br><b>Title:</b><br>" + str(title)

        meta_results = ''

        #loop over result and adds to it the response
        for i in meta:
            meta_results+=html.escape(str(i))+"<br>"
        meta_results = "<b>Metadata:</b><br>" + meta_results


        #find author
        print("[AUTHOR]")
        author = ''
        for i in soup.findAll('meta',{'name':True}):
            if 'author' in i['name']:
                print(i['content'])
                author = i['content']
        author_debug = "<br><br><b>Authors: </b><br>" + author


        #find h1 and h2
        h1 = ''
        print('h1:',soup.h1)
        if soup.h1 != None:
            h1 =  "<br><br><b>h1: </b><br>" + str(soup.h1.string)


        response += meta_results + title_debug + h1 + author_debug


        #put in APA reference
        ref,intext = APA_cite(author,"2017",title,url)




    return render_template('cite.html',debug=response,link=url,references=ref,intext=intext)


def parse_url(url):

    if url.startswith("http://")==0 and url.startswith("https://")==0:
        url="http://"+url

    print("[PARSED URL]:",url)
    return url

def APA_cite(author,released_date,title,url):

    authors = author.split(',')
    for name in authors:
        if len(name.split())>1:
            fname=name.split()[0]
            lname=name.split()[1]

        elif len(name.split())==1:
            fname=name
            lname=0
        else:
            authors=''

    #get date accessed
    date_accessed = datetime.date.today()
    date_accessed = date_accessed.strftime("%d %B %Y")

    #put into APA format
    if len(authors) > 0 :
        if not lname:   #if there is no last name
            ref = "%s. (%s). %s. Retrieved %s, from %s" %(fname.capitalize(),released_date,title,date_accessed,url)
            intext = "%s, %s"%(fname,released_date)

        else:
            ref = "%s, %s. (%s). %s. Retrieved %s, from %s" %(lname,fname[0].upper(),released_date,title,date_accessed,url)
            intext = "%s., %s"%(lname[0].capitalize(),released_date)

    else:
        ref = "%s.(%s). Retrieved %s, from %s" %(title,released_date,date_accessed,url)
        intext = "(\"%s\", %s)"%(title,released_date)

    return ref,intext


if __name__ == '__main__':
    app.run()
