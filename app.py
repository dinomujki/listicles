# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for

from bs4 import BeautifulSoup
import urllib

# Initialize the Flask application
app = Flask(__name__)

# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is 
# accepting: POST requests in this case
@app.route('/List/', methods=['POST'])
def List():
    link=request.form['prompt']
    html=urllib.urlopen(link).read()
    soup=BeautifulSoup(html)
    return render_template('form_action.html', name=soup.prettify()[0:1000])


# Run the app :)
if __name__ == '__main__':
  app.debug = True
  app.run( 
        host="0.0.0.0",
        port=int("8000")
  )
