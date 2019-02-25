from bs4 import BeautifulSoup
import requests
import datetime
import logging
import csv
import re
import urllib.request
import os

def setLogger():
    logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='logs_file',
                    filemode='w')
    console = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def getThread(baseURL, threadid,frompage = 1):

    logging.info("Scraping data for link: {}".format(threadid))

    # get the page and make the soup
    
    url = baseURL + "showthread.php?t=" + str(threadid)
    if frompage > 1:
        url = url + '&page=' + str(frompage)
    
    r = requests.get(url)
    print('get url done : ' + url )
    data = r.text
    soup = BeautifulSoup(data, "lxml")    
    posts = soup.find("div", id ="posts")
    
    return posts

def download_img(posts,baseURL,file_path):
    imgs = posts.findAll("div", {"class":"imageframe flexposts__attachments-imageframe"})
    
    for img in imgs:
        imgUrl = img.a['href'] #.split("imgurl=")[1]
        imgUrl = baseURL + imgUrl
        print(imgUrl)
        urllib.request.urlretrieve(imgUrl, os.path.basename(imgUrl))

if __name__ == '__main__':
    threadid = 792598
    topic = "Most Famous Blessing 3.9.6 EA and Setfiles"
    frompage = 1
    endpage = 36
    baseURL = "https://www.forexfactory.com/"
    file = "./template.html"

    dest = topic + str(threadid) + '-' + str(frompage) + '-' + str(endpage) + '.html'    
    context = ''
    with open(file,'r') as f:
        c = f.read()

    while frompage<= endpage :
        posts = getThread(baseURL, threadid,frompage)
        context += str(posts) + '\n'
        frompage += 1

    context = context.replace('href="','href="' + baseURL )
    context = context.replace('src="attachment.php?attachmentid','src="' + baseURL + 'attachment.php?attachmentid')    

    c = c.replace('endofthread', context + '\n')
    c = c.replace('TitleHere', topic)
    
    with open(dest,'wb') as f:
        f.write(c.encode('ascii', 'xmlcharrefreplace'))
    print('done!')   
