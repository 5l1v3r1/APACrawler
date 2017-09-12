from flask import Flask,request
from bs4 import BeautifulSoup

app = Flask(__name__) #initiates Flask app


#default page
page = '''

    <title>APACrawler -- APA autocite</title>

    <head>

    </head>

    <header>
    <h1>APACrawler</h1>
    <p>Welcome to APACrawler, the APA auto citer 
    powered by Python 3 and flask!</p>
    </header>

    <form method="GET" action="/cite">

            <input type="text" name="url">

            <input type="submit" value="Cite">

    </form>

    '''


@app.route('/') #route is the 'directory'
def main():
    #returns that page
    return page


@app.route('/cite', methods=['GET'])
def cite():
    error = None
    if request.method == 'GET':
        url=request.args.get('url')
        return page+url;
    else:
        return page


if __name__ == '__main__':
    app.run()
