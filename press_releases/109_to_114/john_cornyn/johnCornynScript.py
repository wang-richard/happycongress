# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:22:12 2019

@author: Richard
"""

from bs4 import BeautifulSoup
import requests
from datetime import datetime

headers = requests.utils.default_headers()

headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
)

baseURL = 'https://www.cornyn.senate.gov/newsroom?field_news_category_tid=1&page='
urlsList = []
errorsList = []
for counter in range(1, 186):
    print "URL counter: "+str(counter)
    targetURL = baseURL+str(counter)+'&'
    try:
        response = requests.get(targetURL, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, 'html5lib')
        a = soup.find('div',attrs={"class":"view-content"})
        b = a.findAll('a')
        for link in b:
            url = link.attrs['href']
            url = url.strip()
            pressURL = 'https://www.cornyn.senate.gov'+url
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
        a = soup.find('div',attrs={"class":"col-sm-6"})
        date = a.get_text()
        date = date.replace('\r', ' ').replace('\n', ' ').replace('\t',' ')
        date = date.strip()
        date = date[-10:]
        date = datetime.strptime(date, "%m/%d/%Y").strftime("%m.%d.%Y")
        
        #Grabbing the text for press release:
        a = soup.find('div',attrs={"class":"field field-name-body field-type-text-with-summary field-label-hidden"})
        
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
    counter += 1

text_file = open("johnCornynPress.txt", "w")
for press in pressList:
    text_file.write(press.encode('utf-8')+"\n")
text_file.close()

text_file = open("johnCornynPressErrors.txt", "w")
for error in errorsList:
    text_file.write(error.encode('utf-8')+"\n")
text_file.close()