# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for

from bs4 import BeautifulSoup
import urllib, urllib2

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
    outputprompt=request.form['prompt']

    prompts = outputprompt.split()
    prompt="+".join(prompts)

    # use bing to find url of wikipedia list from prompt
    bingurl = "https://www.bing.com/search?q=wikipedia+top+ten+list+"+str(prompt)
    searchrequest = urllib2.Request(bingurl, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urllib2.urlopen(searchrequest)
    page = urlfile.read()
    soup = BeautifulSoup(page)
    k=soup.find('ol', id="b_results").a['href']
    wikiurl=k
    print wikiurl

    # scrape wiki url
    html=urllib.urlopen(wikiurl).read()
    soup=BeautifulSoup(html)

    l = soup.find('table', class_='wikitable')
    # l = soup.find('table')
    # print l

    # rawitems = l.find_all('th', {'scope':'row'})[0:10]
    rawitems = l.find_all('tr')[0:15]
    # print rawitems

    names = []
    descs = []
    imgs = []
    counter = 0

    for item in rawitems:
        if counter == 10:
            break
        if len(item.find_all('td')) != 0 and len(item.find_all('a')) > 0: #row in table
            scoperow = item.find_all('th', {'scope':'row'})
            if len(scoperow) > 0:
                linkitem = scoperow[0].find('a', class_=lambda x: x != 'reference')
            else:
                linkitem = item.find('a')
            print linkitem
            name = linkitem.contents[0]
            linkurl = linkitem['href']
            print name
            #   name['href']="http://www.imdb.com/"+name['href']
            names.append(name)

            # # names[counter]="http://www.imdb.com/"+names[counter]
            # googlenames = str(item.find('a').get_text().encode('ascii','ignore'))
            # googlenameslist = googlenames.split()
            # googlenames = "+".join(googlenameslist)
            # #   googleurl = "https://www.google.com/search?q=wikipedia+"+str(googlenames)+"+film"
            # googleurl = "https://www.bing.com/search?q=wikipedia+"+str(googlenames)
            #
            # searchrequest = urllib2.Request(googleurl, None, {'User-Agent':'Mosilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
            wikiurl = "http://en.wikipedia.org" + str(linkurl)
            # urlfile = urllib2.urlopen(linkurl)
            # page = urlfile.read()
            #
            # soup=BeautifulSoup(page)
            # # wikiurl=soup.find('h3', class_="r")
            # # wikiurl=wikiurl.find('a')
            # # wikiurl=wikiurl['href']

            deschtml=urllib.urlopen(wikiurl).read()
            soup=BeautifulSoup(deschtml)
            # k=(soup.find_all('div', class_='mw-content-ltr')[0]).find('p')
            k=soup.find_all('div', class_='mw-content-ltr')[0].find('p', recursive=False)
            descs.append(k)

            img=(soup.find('div', class_='mw-content-ltr')).find('img')
            imgs.append(img)

            counter=counter+1
            #   descs.append(str(item.find('span', class_='outline').get_text()))


    return render_template('form_action.html', prompt=outputprompt, image0 = imgs[0],image1 = imgs[1],image2 = imgs[2],image3 = imgs[3],image4 = imgs[4],image5 = imgs[5],image6 = imgs[6],image7 = imgs[7],image8 = imgs[8],image9 = imgs[9], name0=names[0], name1=names[1], name2=names[2],name3=names[3],name4=names[4],name5=names[5],name6=names[6],name7=names[7],name8=names[8],name9=names[9], desc0=descs[0], desc1=descs[1], desc2=descs[2], desc3=descs[3], desc4=descs[4], desc5=descs[5], desc6=descs[6], desc7=descs[7], desc8=descs[8], desc9=descs[9])
    # return render_template('form_action.html', prompt=prompt,name0=names[0], name1=names[1], name2=names[2],name3=names[3],name4=names[4],name5=names[5],name6=names[6],name7=names[7],name8=names[8],name9=names[9], desc0=descs[0], desc1=descs[1], desc2=descs[2], desc3=descs[3], desc4=descs[4], desc5=descs[5], desc6=descs[6], desc7=descs[7], desc8=descs[8], desc9=descs[9])
    # return render_template('form_action.html', prompt=prompt,name0=names[0], name1=names[1], name2=names[2],name3=names[3],name4=names[4],name5=names[5],name6=names[6],name7=names[7],name8=names[8],name9=names[9])
    # return render_template('form_action.html', prompt=prompt)


# Run the app :)
if __name__ == '__main__':
  app.debug = True
  app.run(
        host="0.0.0.0",
        port=int("8000")
  )
