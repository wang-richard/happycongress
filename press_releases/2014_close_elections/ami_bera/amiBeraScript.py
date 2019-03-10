# -*- coding: utf-8 -*-
"""
Created on Sat Mar 09 13:34:41 2019

@author: Richard
"""

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.parser import parse

headers = requests.utils.default_headers()

headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
)

baseURL = 'https://bera.house.gov/media-center/press-releases?page='
urlsList = []
errorsList = []
for counter in range(1, 20):
    print "URL counter: "+str(counter)
    targetURL = baseURL+str(counter)
    try:
        response = requests.get(targetURL, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, 'html5lib')
        a = soup.findAll('h3',attrs={"class":"field-content"})
        for link in a:
            url = link.find('a').attrs['href']
            url = url.strip()
            pressURL = 'https://bera.house.gov'+url
            urlsList.append(pressURL)
    
    except:
        print "error has occurred at "+str(counter)
        errorsList.append(targetURL)
        pass

counter = 0
pressList = []
for targetURL in urlsList:
    print "Press Release counter: "+str(counter)
    string = ''
    try:
        response = requests.get(targetURL, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, 'html5lib')
        
        #Grabbing the date-stamp for press release:
        a = soup.find('div', attrs={"class":"panel-pane pane-node-created"})
        date = a.get_text()
        date = date.strip()
        date = parse(date)
        date = str(date)
        date = date[0:10]
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%m.%d.%Y")
        
        #Grabbing the text for press release:
        a = soup.find('div',attrs={"class":"panel-pane pane-entity-field pane-node-body"})
        [x.extract() for x in a.findAll('script')]
        [x.extract() for x in a.findAll('style')]
        [x.extract() for x in a.findAll("span", {'class':'hidden'})]  
        [x.extract() for x in a.findAll("div", {'class':'hidden'})]  
        
        string += a.get_text()
    
    except:
        print "error has occurred with url: "+str(targetURL)
        errorsList.append(targetURL)
        pass

    string = string.replace('\r', ' ').replace('\n', ' ').replace('\t',' ')
    string = string.strip()
    string = ' '.join(string.split())
    pressList.append(date+'\t'+string)
    counter+=1

text_file = open("amiBeraPress.txt", "w")
for press in pressList:
    text_file.write(press.encode('utf-8')+"\n")
text_file.close()

text_file = open("amiBeraPressErrors.txt", "w")
for error in errorsList:
    text_file.write(error.encode('utf-8')+"\n")
text_file.close()
