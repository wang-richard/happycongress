# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 09:06:15 2019

@author: Richard
"""

from bs4 import BeautifulSoup
import requests
from datetime import datetime
from dateutil.parser import parse
import re

headers = requests.utils.default_headers()

headers.update(
        {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
        }
)

baseURL = 'https://cuellar.house.gov/news/documentquery.aspx?DocumentTypeID=1232&Page='
urlsList = []
errorsList = []
for counter in range(1, 158):
    print "URL counter: "+str(counter)
    targetURL = baseURL+str(counter)
    try:
        response = requests.get(targetURL, headers=headers)
        text = response.text
        soup = BeautifulSoup(text, 'html5lib')
        a = soup.findAll('h3',attrs={"class":"newsie-titler"})
        for link in a:
            url = link.find('a').attrs['href']
            url = url.strip()
            pressURL = 'https://cuellar.house.gov/news/'+url
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
        a = soup.find('div', attrs={"class":"topnewstext"})
        date = a.get_text()
        date = date.strip()
        date = re.search(r'\b(Jan(uary)?|Feb(ruary)?|Mar(ch)?|Apr(il)?|May|Jun(e)?|Jul(y)?|Aug(ust)?|Sep(tember)?|Oct(ober)?|Nov(ember)?|Dec(ember)?)\s+\d{1,2},\s+\d{4}', date).group()
        date = parse(date)
        date = str(date)
        date = date[0:10]
        date = datetime.strptime(date, "%Y-%m-%d").strftime("%m.%d.%Y")
        
        #Grabbing the text for press release:
        a = soup.find('div',attrs={"class":"bodycopy"})
        
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

text_file = open("henryCuellarPress.txt", "w")
for press in pressList:
    text_file.write(press.encode('utf-8')+"\n")
text_file.close()

text_file = open("henryCuellarPressErrors.txt", "w")
for error in errorsList:
    text_file.write(error.encode('utf-8')+"\n")
text_file.close()