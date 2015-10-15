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
    l = soup.find_all('div', class_='article')[0]
    print l
    # tbody = l.find_all('tbody')[0]
    rawitems = l.find_all('td', class_="title")[0:10]
    items = []
    for item in rawitems:
      title = item.find('a').contents[0]
      desc = item.find('span', class_='outline').get_text()
      items.append(str(title) + ": " + str(desc))
  
    return render_template('form_action.html', name0=items[0], name1=items[1], name2=items[2],name3=items[3],name4=items[4],name5=items[5],name6=items[6],name7=items[7],name8=items[8],name9=items[9])
    # return render_template('form_action.html', name=rawitems)

# Run the app :)
if __name__ == '__main__':
  app.debug = True
  app.run( 
        host="0.0.0.0",
        port=int("8000")
  )
