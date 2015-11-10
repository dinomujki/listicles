# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates
from flask import Flask, render_template, request, url_for
import re
from bs4 import BeautifulSoup
import urllib, urllib2
import requests
import html5lib
# Initialize the Flask application
app = Flask(__name__)


import sys
reload(sys)  
sys.setdefaultencoding('utf8')


# Define a route for the default URL, which loads the form
@app.route('/')
def form():
    return render_template('form_submit.html')

# Define a route for the action of the form, for example '/hello/'
# We are also defining which type of requests this route is
# accepting: POST requests in this case
@app.route('/List/', methods=['POST'])
def List():
    inputprompt=request.form['prompt']
    prompts = inputprompt.split()
    prompt1="+".join(prompts)

    inputmetric=request.form['metric']
    prompts = inputmetric.split()
    prompt2="+".join(prompts)
    # youtubeurl = "https://www.youtube.com/results?search_query=documentary+top+"+str(prompt)
    # # searchrequest = urllib2.Request(youtubeurl, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    # urlfile = urllib2.urlopen(youtubeurl)
    # page = urlfile.read()
    # soup = BeautifulSoup(page)
    # # vidlink=soup.pretiffy()
    # print soup
    


    # use bing to find url of wikipedia list from prompt
    bingurl = "https://www.bing.com/search?q=wikipedia+top+ten+list+of+"+str(prompt1)+"+by+"+str(prompt2)
    print bingurl
    # searchrequest = urllib2.Request(bingurl, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urllib2.urlopen(bingurl)
    page = urlfile.read()
    soup = BeautifulSoup(page)
    # prin  t soup.prettify()
    wikiurl=soup.find('ol', id="b_results").a['href']
    print wikiurl


    # scrape wiki url
    html=urllib.urlopen(wikiurl).read()
    soup=BeautifulSoup(html)

    general=soup.find_all('p')[0:3]
    generaldesc = " "
    breaking = " <br/> <br/> "
    for item in general:
        generaldesc=generaldesc+breaking+item.get_text()



    wikitables = soup.find_all('table', class_='wikitable')

    counter =0
    if (len(wikitables)==0):
        return render_template('failed.html')

    wtable=wikitables[counter]

    while (len(wtable)<9):
        counter+=1
        print "counter=",counter
        if (counter==len(wikitables)):
            return render_template('failed.html')
        wtable=wikitables[counter]

    if (str(wtable.find('td').get_text())=="."):
        wtable=wikitables[counter+1]



    
    
    
    # rawitems = l.find_all('th', {'scope':'row'})[0:10]
    rawitems = wtable.find_all('tr')
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
            names.append(name)

            
            query = name
            query= query.split()
            query='+'.join(query)
            url = "http://www.bing.com/images/search?q=" +(prompt1) + "+" + query + "&qft=+filterui:aspect-square"
            print url
            searchrequest = urllib2.Request(url, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
            urlfile = urllib2.urlopen(searchrequest)
            page = urlfile.read()
            soup = BeautifulSoup(page)
            divsoup = soup.find_all('div', class_='dg_u')[0:5]
            

            wikiurl = "http://en.wikipedia.org" + str(linkurl)

            deschtml=urllib.urlopen(wikiurl).read()
            soup=BeautifulSoup(deschtml)
            # k=(soup.find_all('div', class_='mw-content-ltr')[0]).find('p')
            k=soup.find_all('div', class_='mw-content-ltr')[0].find_all('p', recursive=False)
            if (len(k)==0):
                descs.append(" ")
                imgs.append("None")
            else:
                count1 = 1;
                count2 = 0;
                description = k[0].get_text()
                breaking = " <br/> <br/> "

                while (count1<len(k))&(count2<2):
                    # print "count=", count1
                    par = k[count1].get_text()
                    words = (par.split()) #split the paragraph into individual words
                    if inputmetric in words: #see if one of the words in the paragraph is the word we want
                        description = description+breaking+par
                        count2+=1
                    count1+=1

                descs.append(description)


                linkimg = divsoup[0].find('a')
                linkimg = linkimg['m']
                m = re.search('imgurl:"(.+?)"', linkimg)
                imag = m.group(1)
                print imag
                imgs.append(imag)
                # img=soup.find('   div', class_='mw-content-ltr'    ).find('img')
                # img=soup.find('div', class_='mw-content-ltr').find('img', {'src' : re.compile(r'(jpe?g)$')})

                # counter=0
                # def check_url(url):
                #     return True
                # while (not check_url(imag))&(counter<5):
                #     counter+= 1
                #     linkimg = divsoup[counter].find('a')
                #     linkimg = linkimg['m']
                #     print linkimg
                #     m = re.search('imgurl:"(.+?)"', linkimg)
                #     imag = m.group(1)
                #     print imag

            counter+=1
    while (counter<11):
        names.append(" ")
        descs.append(" ")
        imgs.append(" ")
        counter+=1  



        

    return render_template('form_action.html', prompt=inputprompt, metric=inputmetric, generaldesc=generaldesc, image0 = imgs[0],image1 = imgs[1],image2 = imgs[2],image3 = imgs[3],image4 = imgs[4],image5 = imgs[5],image6 = imgs[6],image7 = imgs[7],image8 = imgs[8],image9 = imgs[9], name0=names[0], name1=names[1], name2=names[2],name3=names[3],name4=names[4],name5=names[5],name6=names[6],name7=names[7],name8=names[8],name9=names[9], desc0=descs[0], desc1=descs[1], desc2=descs[2], desc3=descs[3], desc4=descs[4], desc5=descs[5], desc6=descs[6], desc7=descs[7], desc8=descs[8], desc9=descs[9])
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
