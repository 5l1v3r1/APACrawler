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
        print("url:",url)

        #get the content of the URL
        try:
            source = urllib.request.urlopen(url)
        except urllib.error.URLError:
            return render_template("index.html") + "Cannot find URL specified."

        #start parsing it with BeautifulSoup
        soup = BeautifulSoup(source, 'html.parser')
        #find all instances of <meta> (for metadata) in the soup
        meta = soup.find_all("meta")


        #find the title
        title = find_title(soup)

        meta_results = ''

        #loop over result and adds to it the response
        for i in meta:
            meta_results+=html.escape(str(i))+"<br>"
        meta_results = "<b>Metadata:</b><br>" + meta_results


        #find authors
        authors_list = find_authors(soup)
        #author debug info
        author_debug = ''
        for author in authors_list:
            author_debug +=  ", ".join(author) + '\n'


        #find h1 and h2
        h1 = ''
        if soup.h1 != None:
            h1 =  "<br><br><b>h1: </b><br>" + str(soup.h1.string)


        response += meta_results + h1


        #put in APA reference
        ref,intext = APA_cite(authors_list,"2017",title,url)


    return render_template('cite.html',
        debug=response,
        link=url,
        references=ref,
        intext=intext,
        title=title,
        authors=author_debug)


def parse_url(url):
    '''This function parses the URL according to what it starts with.'''

    if url.startswith("http://")==0 and url.startswith("https://")==0:
        url="http://"+url

    return url



def find_title(soup):
    '''finds the title of the site in the soup'''
    #gets the <title>
    title_tag = soup.title.string

    og_title = 0
    #finds og_title (a property in metatdata used for facebook)
    for i in soup.findAll('meta',{'property':True}):
        if "og:title" in i['property']:
            og_title = i['content']

    try:
        h1 = soup.h1.string
    except:
        h1 = 0

    if og_title==0 and h1==0:
        title = title_tag

    elif og_title==0:
        title = h1

    else:
        title=og_title
        

    print("[In find_title] title:",title)

    return title



def find_authors(soup):
    '''find authors in the soup'''
    authors = []
    authors_list = []

    for i in soup.findAll('meta',{'name':True}):
        if 'author' in i['name']:
            authors.append(i['content'])
        if 'DC.Creator' in i['name']:
            authors.append(i['content'])

    for author in authors:   #to cater for multiple authors

        #split the author name by space
        fullname = author.split() 

        #lastname is the last element of the full name
        lastname = fullname[-1]

        othernames = fullname[0:-1]
        #take only the capitalized first character
        othernames = [ (name.capitalize()[0]+".") for name in othernames]

        #put lastname and othernames(as a bracket separated string) into a list called author
        author = [lastname, (" ").join(othernames)]

        #append the author to authors_list as a sublist
        authors_list.append(author)

    return authors_list


def APA_cite(authors_list,released_date,title,url):
    '''use all the given arguments to generate APA bibliography and in-text reference, as well as insert date accessed to current date.'''

    #parse authors
    i=1
    authors_str = ''
    intext_author = ''
    if 1 < len(authors_list) <= 7:
        for author in authors_list:

            if i == len(authors_list): #on the last author
                author_str += "& " + author[0] + ", "+ author[1]
                intext_author += author[0]


            authors_str += author[0]+", "+author[1]+", "
            i+=1
            intext_author += author[0] + "&"

    elif len(authors_list) == 1:
        for author in authors_list:
            authors_str += author[0] + ", " + author[1]

        intext_author += author[0]





    #get date accessed
    date_accessed = datetime.date.today()
    date_accessed = date_accessed.strftime("%d %B %Y")

    #put into APA format
    if authors_str != '':

        ref = "%s (%s). <i>%s</i>. Retrieved %s, from %s" %(authors_str,released_date,title,date_accessed,url)
        intext = "(%s, %s)"%(intext_author,released_date)

    else:
        ref = "<i>%s</i>. (%s). Retrieved %s, from %s" %(title,released_date,date_accessed,url)
        intext = "(\"%s\", %s)"%(title,released_date)

    return ref,intext





if __name__ == '__main__':
    app.run()
