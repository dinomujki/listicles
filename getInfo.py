from bs4 import BeautifulSoup
import urllib, urllib2
import requests
import html5lib
import lxml

def getInfo(prompt1, linkitem, counter, names, descs, imgs, infos, tabledata, inputmetric, tableheaders):
    if linkitem == None:
        name = tabledata[counter][1]
        descs.append("")

    else:
        name = linkitem.contents[0]

        # check if we can get descs
        linkurl = linkitem['href']
        wikiurl = "http://en.wikipedia.org" + str(linkurl)
        print wikiurl
        goodurl=check_url(wikiurl)

        if goodurl:
            getItemDescription(descs, wikiurl, counter, tableheaders, tabledata, inputmetric)
        else:
            descs.append(" ")

    # append name
    names.append(name)

    # get infos
    getItemInfo(infos, counter, tableheaders, tabledata)

    # get images
    getImage(imgs, name, prompt1)


def getImage(imgs, name, prompt1):
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
        imag = linkimg
    else:
        imag = None
    imgs.append(imag)

def getItemDescription(descs, wikiurl, counter, tableheaders, tabledata, inputmetric):
    # get descs
    deschtml=urllib.urlopen(wikiurl).read()
    soup=BeautifulSoup(deschtml, "lxml")
    k=soup.find_all('div', class_='mw-content-ltr')
    if (len(k)==0):
        descs.append(" ")

    else:
        k=k[0].find_all('p', recursive=False)
        count1 = 1;
        count2 = 0;

        breaking = " <br/> <br/> "
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

def getItemInfo(infos, counter, tableheaders, tabledata):
    breaking = "<br/> <br/>"
    info = ""
    for index, item in enumerate(tabledata[counter]):
        temp = str(tableheaders[index].split('[')[0]) + ": " + str(item) + "<br/>"
        info += temp
    info += breaking
    infos.append(info)

def check_url(url):
    if (url != "") and ("redlink=1" not in url) and ('endnote' not in url):
        return True
    return False
