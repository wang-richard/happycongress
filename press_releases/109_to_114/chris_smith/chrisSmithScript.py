# -*- coding: utf-8 -*-
"""
Created on Mon Mar 11 14:08:57 2019

@author: lilly
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

baseURL = 'https://chrissmith.house.gov/news/documentquery.aspx?Year='

urlsList = []
errorsList = []
for year in range(2005, 2019):
    if year == 2005:
        endPage = 15
    
    elif year == 2006:
        endPage = 14
    
    elif year == 2007:
        endPage = 15
                
    elif year == 2008:
        endPage = 7
                
    elif year == 2009:
        endPage = 11
                
    elif year == 2010:
        endPage = 10        
                
    elif year == 2011:
        endPage = 19
                
    elif year == 2012:
        endPage = 21
            
    elif year == 2013:
        endPage = 24
    
    elif year == 2014:
        endPage = 25
            
    elif year == 2015:
        endPage = 28

    elif year == 2016:
        endPage = 33

    elif year == 2017:
       endPage = 29
    
    elif year == 2018:
        endPage = 27
    
    for counter in range(1, endPage):
        print "URL counter: "+str(year)+" "+str(counter)
        targetURL = baseURL + str(year) + '&Page=' + str(counter)
        try:
            response = requests.get(targetURL, headers=headers)
            text = response.text
            soup = BeautifulSoup(text, 'html5lib')
            a = soup.findAll('a',attrs={"class":"middleheadline"})
            for link in a:
                url = link.attrs['href']
                url = url.strip()
                pressURL = 'https://chrissmith.house.gov/news/'+url
                urlsList.append(pressURL)
        except:
            print "error has occurred at "+str(year)+" "+str(counter)
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

text_file = open("chrisSmithPress.txt", "w")
for press in pressList:
    text_file.write(press.encode('utf-8')+"\n")
text_file.close()

text_file = open("chrisSmithPressErrors.txt", "w")
for error in errorsList:
    text_file.write(error.encode('utf-8')+"\n")
text_file.close()