# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 15:31:19 2018
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

targetURL = 'https://frelinghuysen.house.gov/top-news/'
urlsList = []
errorsList = []
response = requests.get(targetURL, headers=headers)
text = response.text
soup = BeautifulSoup(text, 'html5lib')
a = soup.findAll('li',attrs={"class":"article"})
for link in a:
    url = link.find('a').attrs['href']
    url = url.strip()
    pressURL = 'https://frelinghuysen.house.gov'+url
    urlsList.append(pressURL)

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
        a = soup.find('span', attrs={"class":"contentdate"})
        date = a.get_text()
        date = date.strip()
        date = parse(date)
        date = str(date)
        date = date[0:10]
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%m.%d.%Y")
        
        #Grabbing the text for press release:
        a = soup.find('div',attrs={"class":"contentdata"})
        
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

text_file = open("rodneyFrelinghuysenPress.txt", "w")
for press in pressList:
    text_file.write(press.encode('utf-8')+"\n")
text_file.close()

text_file = open("rodneyFrelinghuysenPressErrors.txt", "w")
for error in errorsList:
    text_file.write(error.encode('utf-8')+"\n")
text_file.close()