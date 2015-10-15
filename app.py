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
    url = "http://www.imdb.com/genre/" + str(link)
    html=urllib.urlopen(url).read()
    soup=BeautifulSoup(html)
    l = soup.find_all('div', class_='article')[0]
    print l
    # tbody = l.find_all('tbody')[0]
    rawitems = l.find_all('td', class_="title")[0:10]
    names = []
    descs= []
    for item in rawitems:
      names.append(str(item.find('a').contents[0]))
      descs.append(str(item.find('span', class_='outline').get_text()))

  
    return render_template('form_action.html', prompt=link, name0=names[0], name1=names[1], name2=names[2],name3=names[3],name4=names[4],name5=names[5],name6=names[6],name7=names[7],name8=names[8],name9=names[9], desc0=descs[0], desc1=descs[1], desc2=descs[2], desc3=descs[3], desc4=descs[4], desc5=descs[5], desc6=descs[6], desc7=descs[7], desc8=descs[8], desc9=descs[9])
    # return render_template('form_action.html', name=rawitems)

# Run the app :)
if __name__ == '__main__':
  app.debug = True
  app.run( 
        host="0.0.0.0",
        port=int("8000")
  )
