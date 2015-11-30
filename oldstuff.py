

# ______________________________________________________________________________________________________________________________________________________________________________________________
# ____________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________________________________________________________________________________











# youtubeurl = "https://www.youtube.com/results?search_query=documentary+top+"+str(prompt)
# # searchrequest = urllib2.Request(youtubeurl, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
# urlfile = urllib2.urlopen(youtubeurl)
# page = urlfile.read()
# soup = BeautifulSoup(page)
# # vidlink=soup.pretiffy()
# print soup

    # linkitem = scoperow[0].find('td').find('a', class_=lambda x: x != 'reference', recursive=False)
# linkitem = scoperow[0].find('a', class_=lambda x: x != 'reference')
# linkitems = scoperow[0].find_all('td')
# for item in linkitems:
#     if len(item.find_all('a')) > 0:
#         linkitem = item.find('a', class_=lambda x: x != 'reference', recursive=False)
#     break

# linkitems = item.find_all('td')
                # for item in linkitems:
                #     if len(item.find_all('a')) > 0:
                #         linkitem = item.find('a', recursive=False)
                #     break

# counter = 10 - len(names)
    # while counter > 0:
    #     if counter == 10:
    #         break
    #     if len(item.find_all('td')) != 0 and len(item.find_all('a')) > 0: #row in table
    #         scoperow = item.find_all('th', {'scope':'row'})
    #         if len(scoperow) > 0:

    #             linkitem = item.find('a', class_=lambda x: x != 'reference')
    #         else:

    #             linkitem = item.find('a')

    #         print linkitem

    #         name = linkitem.contents[0]

    #         linkurl = linkitem['href']
    #         print name
    #         names.append(name)


    #         query = str(name)
    #         if len(query) > 1:
    #             query = query.split()
    #             query='+'.join(query)
    #         url = "http://www.bing.com/images/search?q=" + prompt1 + "+" + query + "&qft=+filterui:aspect-square+filterui:imagesize-wallpaper&FORM=R5IR3"
    #         print url
    #         searchrequest = urllib2.Request(url, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    #         urlfile = urllib2.urlopen(searchrequest)
    #         page = urlfile.read()
    #         soup = BeautifulSoup(page, 'lxml')


    #         divsoup = soup.find_all('div', class_='dg_u')

    #         wikiurl = "http://en.wikipedia.org" + str(linkurl)

    #         deschtml=urllib.urlopen(wikiurl).read()
    #         soup=BeautifulSoup(deschtml)
    #         # k=(soup.find_all('div', class_='mw-content-ltr')[0]).find('p')
    #         k=soup.find_all('div', class_='mw-content-ltr')[0].find_all('p', recursive=False)
    #         if (len(k)==0):
    #             descs.append(" ")
    #             imgs.append("None")
    #         else:
    #             count1 = 1;
    #             count2 = 0;

    #             breaking = " <br/> <br/> "
    #             info = ""
    #             for index, item in enumerate(tabledata[counter + 1]):
    #                 temp = str(tabledata[0][index]) + ": " + str(item) + "<br/>"
    #                 info += temp
    #             info += breaking
    #             infos.append(info)

    #             description = k[0].get_text()


    #             while (count1<len(k))&(count2<2):
    #                 # print "count=", count1
    #                 par = k[count1].get_text()
    #                 words = (par.split()) #split the paragraph into individual words
    #                 if inputmetric in words: #see if one of the words in the paragraph is the word we want
    #                     description = description+breaking+par
    #                     count2+=1
    #                 count1+=1

    #             descs.append(description)

    #             if (len(divsoup)>0):
    #                 linkimg = divsoup[0].find('a')
    #                 linkimg = linkimg['m']
    #                 m = re.search('imgurl:"(.+?)"', linkimg)
    #                 imag = m.group(1)
    #             else:
    #                 imag="None"

    #             print imag
    #             imgs.append(imag)

    #             # # img=soup.find('div', class_='mw-content-ltr').find('img')
    #             # img=soup.find('div', class_='mw-content-ltr').find('img', {'src' : re.compile(r'(jpe?g)$')})
    #             #
    #             # counter=0
    #             # def check_url(url):
    #             #     return True
    #             # while (not check_url(imag))&(counter<5):
    #             #     counter+= 1
    #             #     linkimg = divsoup[counter].find('a')
    #             #     linkimg = linkimg['m']
    #             #     print linkimg
    #             #     m = re.search('imgurl:"(.+?)"', linkimg)
    #             #     imag = m.group(1)
    #             #     print imag

    #         counter+=1
    # while (counter<11):
    #     names.append(" ")
    #     descs.append(" ")
    #     imgs.append(" ")
    #     infos.append(" ")
    #     counter+=1


    # for item in rawitems:
    #     # print item
    #
    #     if counter == 10:
    #         break
    #     if len(item.find_all('td')) != 0 and len(item.find_all('a')) > 0: #row in table
    #         scoperow = item.find_all('th', {'scope':'row'})
    #         if len(scoperow) > 0:
    #             # linkitem = scoperow[0].find('td').find('a', class_=lambda x: x != 'reference', recursive=False)
    #             # linkitem = scoperow[0].find('a', class_=lambda x: x != 'reference')
    #             # linkitems = scoperow[0].find_all('td')
    #             # for item in linkitems:
    #             #     if len(item.find_all('a')) > 0:
    #             #         linkitem = item.find('a', class_=lambda x: x != 'reference', recursive=False)
    #             #     break
    #             linkitem = scoperow[0].find('a', class_=lambda x: x != 'reference', recursive=False)
    #         else:
    #             # linkitems = item.find_all('td')
    #             # for item in linkitems:
    #             #     if len(item.find_all('a')) > 0:
    #             #         linkitem = item.find('a', recursive=False)
    #             #     break
    #             linkitem = item.find('a')
    #
    #         # print linkitem
    #
    #         name = linkitem.contents[0]
    #
    #         linkurl = linkitem['href']
    #         print name
    #         names.append(name)
    #
    #
    #         query = str(name)
    #         if len(query) > 1:
    #             query = query.split()
    #             query='+'.join(query)
    #         url = "http://www.bing.com/images/search?q=" + prompt1 + "+" + query + "&qft=+filterui:aspect-square"
    #         print url
    #         searchrequest = urllib2.Request(url, None, {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_7_4) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11'})
    #         urlfile = urllib2.urlopen(searchrequest)
    #         page = urlfile.read()
    #         # soup = BeautifulSoup(page, 'lxml').find('body').find("div", {"id":"b_content"})
    #         soup = BeautifulSoup(page, 'lxml')
    #
    #
    #         divsoup = soup.find_all('div', class_='dg_u')
    #
    #         wikiurl = "http://en.wikipedia.org" + str(linkurl)
    #
    #         deschtml=urllib.urlopen(wikiurl).read()
    #         soup=BeautifulSoup(deschtml)
    #         # k=(soup.find_all('div', class_='mw-content-ltr')[0]).find('p')
    #         k=soup.find_all('div', class_='mw-content-ltr')[0].find_all('p', recursive=False)
    #         if (len(k)==0):
    #             descs.append(" ")
    #             imgs.append("None")
    #         else:
    #             count1 = 1;
    #             count2 = 0;
    #
    #             breaking = " <br/> <br/> "
    #             info = ""
    #             for index, item in enumerate(tabledata[counter + 1]):
    #                 temp = str(tabledata[0][index]) + ": " + str(item) + "<br/>"
    #                 info += temp
    #             info += breaking
    #             infos.append(info)
    #
    #             description = k[0].get_text()
    #
    #
    #             while (count1<len(k))&(count2<2):
    #                 # print "count=", count1
    #                 par = k[count1].get_text()
    #                 words = (par.split()) #split the paragraph into individual words
    #                 if inputmetric in words: #see if one of the words in the paragraph is the word we want
    #                     description = description+breaking+par
    #                     count2+=1
    #                 count1+=1
    #
    #             descs.append(description)
    #
    #
    #             linkimg = divsoup[0].find('a')
    #             linkimg = linkimg['m']
    #             m = re.search('imgurl:"(.+?)"', linkimg)
    #             imag = m.group(1)
    #             print imag
    #             imgs.append(imag)
    #
    #             # # img=soup.find('div', class_='mw-content-ltr').find('img')
    #             # img=soup.find('div', class_='mw-content-ltr').find('img', {'src' : re.compile(r'(jpe?g)$')})
    #             #
    #             # counter=0
    #             # def check_url(url):
    #             #     return True
    #             # while (not check_url(imag))&(counter<5):
    #             #     counter+= 1
    #             #     linkimg = divsoup[counter].find('a')
    #             #     linkimg = linkimg['m']
    #             #     print linkimg
    #             #     m = re.search('imgurl:"(.+?)"', linkimg)
    #             #     imag = m.group(1)
    #             #     print imag
    #
    #         counter+=1
    # while (counter<11):
    #     names.append(" ")
    #     descs.append(" ")
    #     imgs.append(" ")
    #     counter+=1