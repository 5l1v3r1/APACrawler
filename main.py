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
    if request.method == 'GET':

        url=request.args.get('url')
        
        #parse validity of url
        url=parse_url(url)
        print(url)

        #get the content of the URL
        response = urllib.request.urlopen(url)
        #start parsing it with BeautifulSoup
        soup = BeautifulSoup(response, 'html.parser')
        #find all instances of <meta> (for metadata) in the code
        result = soup.find_all("meta")

        results= ''
        for i in result:
            print(str(i))

        #loop over result and adds to it the response
        for i in result:
            results+=html.escape(str(i))+"<br>"


        return page + results


    else:
        return page

def parse_url(url):

    if url.startswith("http://")==0 and url.startswith("https://")==0:
        url="http://"+url

    print("[PARSED URL]:",url)
    return url




if __name__ == '__main__':
    app.run()
