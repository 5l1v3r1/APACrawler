from flask import Flask
import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def hello_world():
    page = '''

    <title>APACrawler -- APA autocite</title>

    <header>
    <h1>APACrawler</h1>
    <h2>Welcome to APACrawler, the APA auto citer 
    powered by Python 3 and flask!</h2>


    '''


    return page

if __name__ == '__main__':
    app.run()
