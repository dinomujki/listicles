# -*- coding: utf-8 -*-

# We need to import request to access the details of the POST request
# and render_template, to render our templates (form and response)
# we'll use url_for to get some URLs for the app on the templates

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

from flask import Flask, render_template, request, url_for
import re
from bs4 import BeautifulSoup
import urllib, urllib2
import requests
import html5lib
import lxml

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

    # use bing to find url of wikipedia list from prompt
    bingurl = "https://www.bing.com/search?q=wikipedia+top+ten+list+of+"+str(prompt1)+"+by+"+str(prompt2)+"+wikipedia"
    print bingurl
    # searchrequest = urllib2.Request(bingurl, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    urlfile = urllib2.urlopen(bingurl)
    page = urlfile.read()
    soup = BeautifulSoup(page, "lxml")
    bingpage=soup.find('ol', id="b_results")
    wikiurls = bingpage.find_all('li', class_="b_algo")
    # for item in wikiurls:
    #     print item
    # wikiurl = wikiurls[0].a['href']
    # print "wikiurl", wikiurl
    for link in wikiurls:
        # print "LALALLALALA"
        # print "link = ", link.a['href'].lower()
        # print "what = ", ('category' in link.a['href'].lower())
        if ('category' not in str(link.a['href']).lower()):
            wikiurl = link.a['href'].lower()
            break
    print wikiurl


    # scrape wiki url
    html=urllib.urlopen(wikiurl).read()
    soup=BeautifulSoup(html, "lxml")

    # get general description for page
    general=soup.find_all('p')[0:3]
    generaldesc = " "
    breaking = " <br/> <br/> "
    for item in general:
        generaldesc+=breaking+item.get_text()

    # find tables on page, fail if no tables
    wikitables = soup.find_all('table', class_='wikitable')
    if (len(wikitables)==0):
        return render_template('failed.html')

    # pull tables and caption if exists, pull data
    wtable = getTable(wikitables)
    caption = wtable.find('caption')
    if caption==None:
        caption=""
    tableheaders = getHeaders(wtable)
    tabledata = getTabledata(wtable)

    # sort table data
    tableheaders, tabledata = sortTableData(tableheaders, tabledata, inputmetric)


    names = []
    descs = []
    imgs = []
    infos = []
    for index, row in enumerate(tabledata[0:10]):
        getInfo(prompt1, row[-2], index, names, descs, imgs, infos, tabledata, inputmetric, tableheaders)


    for item in [names, descs, imgs, infos]:
        while len(item) < 11:
            item.append("")
        str(item)

    return render_template('form_action.html', prompt=inputprompt, metric=inputmetric, generaldesc=generaldesc, caption=caption, image0 = imgs[0],image1 = imgs[1],image2 = imgs[2],image3 = imgs[3],image4 = imgs[4],image5 = imgs[5],image6 = imgs[6],image7 = imgs[7],image8 = imgs[8],image9 = imgs[9], name0=names[0], name1=names[1], name2=names[2],name3=names[3],name4=names[4],name5=names[5],name6=names[6],name7=names[7],name8=names[8],name9=names[9], desc0=descs[0], desc1=descs[1], desc2=descs[2], desc3=descs[3], desc4=descs[4], desc5=descs[5], desc6=descs[6], desc7=descs[7], desc8=descs[8], desc9=descs[9], info0=infos[0], info1=infos[1], info2=infos[2], info3=infos[3], info4=infos[4], info5=infos[5], info6=infos[6], info7=infos[7], info8=infos[8], info9=infos[9])

def sortTableData(tableheaders, tabledata, inputmetric):
    sorty = False

    # table already sorted
    for index, item in enumerate(tableheaders):
        if "rank" in tableheaders[index].lower():
            tableheaders.append('sortKey')
            for row in tabledata:
                row.append('sorted')
                row[index]=fixstringtoint(row[index])
            tabledata = sorted(tabledata, key=lambda x:x[index], reverse=False)
            sorty=True;
            break

    # look for column that matches input metric to sort on
    if sorty == False:
        for index, item in enumerate(tableheaders):
            metricprompts = inputmetric.split()
            for metric in metricprompts:
                if metric.lower() in item.lower():
                    # if column contains numerical values
                    if len([x for x in tabledata[2][index].split('[')[0].split('(')[0] if x.isdigit()]) > 0:
                        print"TRUEEEEEEEEEEEEEEEEEEEEEEE", tableheaders[index]
                        tableheaders.append('sortKey')

                        for row in tabledata:
                            putin = fixstringtofloat(row[index])
                            row.append(putin)

                        tabledata = sorted(tabledata, key=lambda x:x[-1], reverse=True)
                        sorty = True
                        break
            if sorty:
                break

    # try to find column to sort on
    if sorty == False:
        for index, item in enumerate(tableheaders):
            # make sure this column contains numerical values
            if len([x for x in tabledata[3][index].split('[')[0].split('(')[0] if x.isdigit()]) > 0:
                temp = tabledata[3][index]
                if ("title" not in tableheaders[index].lower())&("year" not in tableheaders[index].lower())&("period" not in tableheaders[index].lower()):
                    if (is_int(temp)):
                        if (int(temp)==1)|(int(temp)==2)|(int(temp)==3)|(int(temp)==4):
                            tableheaders.append('sortKey')
                            for row in tabledata:
                                row.append('sorted')
                            sorty=True;
                            break
                        else:
                            tableheaders.append('sortKey')
                            break;
                    elif ('360' not in temp):
                        tableheaders.append('sortKey')
                        break;
        if sorty == False:
            for row in tabledata:
                putin = fixstringtofloat(row[index])
                row.append(putin)
            tabledata = sorted(tabledata, key=lambda x:x[-1], reverse=True)


    return tableheaders, tabledata

def getTable(wikitables):
    counter = 0
    wtable=wikitables[counter]

    if len(wtable) == 2:
        tempwtable = wtable.find('tbody')
    else:
        tempwtable = wtable
    while (len(tempwtable)<9):
        counter+=1
        print "counter=",counter
        if (counter==len(wikitables)):
            return render_template('failed.html')
        wtable=wikitables[counter]
        if len(wtable) == 2:
            tempwtable = wtable.find('tbody')
        else:
            tempwtable = wtable

    if (str(tempwtable.find('td').get_text())=="."):
        wtable=wikitables[counter+1]
    print "LENGTH OF TABLE = ", len(wtable)
    return wtable

def getHeaders(wtable):
    tableheaders = []
    trows = wtable.find_all('tr')
    header = trows[0].find_all(['th','td'])
    for th in header:
        tableheaders.append(th.get_text())
    tableheaders.append("Wikipedia Link")
    return tableheaders

def fixstring(s):
    s=s.split('[')[0]
    s=s.replace('\n','')
    s=s.split('(')[0]
    if ('\xe2' in s):
        counter = 0
        temp = s
        s=""
        c=temp[counter]
        while (c!='\xe2'):
            counter+=1
            c=temp[counter]
        for c in temp[(counter+1):len(temp)]:
            s+=c
    s=unicode(s, errors='ignore')
    s=s.encode('utf8', 'ignore')
    return s


def getTabledata(wtable):
    tabledata = []
    trows = wtable.find_all('tr')
    for row in trows[1:]:
        # print row.prettify()
        temp = []
        titems = row.find_all(['td', 'th'], recursive=False)
        counter = 0
        for td in titems:
            tdstring = fixstring(str(td.get_text()))
            # print "tdstring=",tdstring
            temp.append(tdstring)

        linkitem = None
        # print "linkitem=",linkitem
        # print row
        linkitems = row.find_all('a')
        if len(linkitems)==0:
            linkitem=None
        else:
            for item in linkitems:
                if "cite" not in str(item) and "citation" not in str(item) and 'image' not in str(item):
                    linkitem = item
                    print "linkitem=",linkitem
                    break

        
        # if linkitem != None:
        temp.append(linkitem)
        if temp != []:
            tabledata.append(temp)
    # print tabledata[0:10]
    return tabledata

def getInfo(prompt1, linkitem, counter, names, descs, imgs, infos, tabledata, inputmetric, tableheaders):
    if linkitem == None:
        goodurl = False;
        breaking = " <br/> <br/> "
        
        info = ""
        print "counter=", counter
        for index, item in enumerate(tabledata[counter]):
            temp = str(tableheaders[index].split('[')[0]) + ": " + str(item) + "<br/>"
            info += temp
            print "info = ", info
        info += breaking
        infos.append(info)
        descs.append("")
        imgs.append("None")
        names.append(tabledata[counter][0]) 
        return   
    else:
        name = linkitem.contents[0]
        linkurl = linkitem['href']
        wikiurl = "http://en.wikipedia.org" + str(linkurl)
        print wikiurl
        goodurl=check_url(wikiurl)

        if 'endnote' in wikiurl:
            goodurl=False
        else:
            goodurl=True

    print "linkitem =", linkitem
    print "goodurl =", goodurl
    if goodurl:
        print name
        names.append(name)


        query = str(name)
        if len(query) > 1:
            query = query.split()
            query='+'.join(query)
        url = "http://www.bing.com/images/search?q=" + prompt1 + "+" + query + "&qft=+filterui:aspect-square+filterui:imagesize-large&FORM=R5IR3"
        print url
        searchrequest = urllib2.Request(url, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
        urlfile = urllib2.urlopen(searchrequest)
        page = urlfile.read()
        soup = BeautifulSoup(page, 'lxml')


        divsoup = soup.find_all('div', class_='dg_u')

        deschtml=urllib.urlopen(wikiurl).read()
        soup=BeautifulSoup(deschtml, "lxml")
        k=soup.find_all('div', class_='mw-content-ltr')
        if (len(k)==0):
            descs.append(" ")
            imgs.append("None")
        else:
            k=k[0].find_all('p', recursive=False)
            count1 = 1;
            count2 = 0;

            breaking = " <br/> <br/> "
            info = ""
            print "counter=", counter
            for index, item in enumerate(tabledata[counter]):
                temp = str(tableheaders[index].split('[')[0]) + ": " + str(item) + "<br/>"
                info += temp
                print "info = ", info
            info += breaking
            infos.append(info)
            description=" "
            if len(k)==0:
                descs.append(" ")
            else:
                description = k[0].get_text()
                while (count1<len(k))&(count2<2):
                    par = k[count1].get_text()
                    words = (par.split()) #split the paragraph into individual words
                    if inputmetric in words: #see if one of the words in the paragraph is the word we want
                        description = description+breaking+par
                        count2+=1
                    count1+=1

            descs.append(description)

            if len(divsoup) > 0:
                # linkimg = divsoup[0].find('a')
                linkimg=None
                imgtag = divsoup[0].find('img')
                if 'src2' in str(imgtag):
                    linkimg = imgtag['src2']
                elif 'src' in str(imgtag):
                    linkimg = imgtag['src']
                # m = re.search('imgurl:"(.+?)"', linkimg)
                # linkimg = linkimg['src']
                print "imag=",linkimg
                imag = linkimg
            else:
                imag = None
            print imag
            imgs.append(imag)
            print names
    else:
        descs.append("")
        imgs.append("None")
        infos.append("")

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def fixstringtoint(s):
    temp=str(s)

    if temp != "":
        temp = temp.split('[')[0]
        temp = temp.split('(')[0]
        temp = temp.split('-')[0]
        temp = temp.split('–')[0]

        temp = temp.split('/')[0]

        truetemp=""
        for c in temp:
            if (c.isdigit()):
                truetemp+=c
        return float(truetemp)
    else:
        return (float('inf'))

def fixstringtofloat(s):
    temp=str(s)
    if temp != "":
        temp = temp.split('[')[0]
        temp = temp.split('(')[0]
        temp = temp.split('-')[0]
        temp = temp.split('–')[0]

        temp = temp.split('/')[0]
        if '!' in temp:
            temp = temp.split('!')[1]
        truetemp=""
        dotty=False
        digity=False
        for c in temp:
            if (c.isdigit()):
                truetemp+=c
                digity=True
            elif (c=="."):
                if digity:
                    if not dotty:
                        truetemp+=c
                        dotty=True
            elif (c==" "):
                if digity:
                    break
        if len(truetemp)>1:
            truetemp = float(re.findall(r"^\d+?\.?\d+?$",truetemp)[0])
        elif len(truetemp)==1:
            truetemp=float(truetemp)
        else:
            truetemp = (float('inf') * -1)
        return truetemp
    else:
        return (float('inf') * -1)


def check_url(url):
    # val = URLValidator(verify_exists=False)
    # try:
    #     val(url)
    #     return True
    # except ValidationError:
    #     return False
    if (url != ""):
        if ("redlink=1" not in url):
            return True
    else:
        return False

# Run the app :)
if __name__ == '__main__':
  app.debug = True
  app.run(
        host="0.0.0.0",
        port=int("8000")
        )
