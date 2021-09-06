
import requests
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import csv
import re
import unicodedata




class GoogleScraper:
    def __init__(self, session, css_id_result, css_id_target):
        self.session = session
        self.css_id_result = css_id_result
        self.css_id_target = css_id_target
    
    def get_data(self):

        with open('keywords.txt') as f:
            keywords = f.read()   
            keywords = keywords.split(', ')

        return keywords
    
    def create_csv(self, file_name, list_name):
        
        with open(file_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list_name)
        
        
class GoogleLinkScraper(GoogleScraper):
        
    def get_links(self, word, n_pages):
        for page in range(1, n_pages):
            response = self.session.get("http://www.google.com/search?q=site:https://www.searchenginejournal.com/" + ' ' + word + "&start=" + str((page - 1) * 10))
            results = response.html.find(self.css_id_result)

            for result in results:
                yield result.find(self.css_id_target, first=True).attrs['href']

    def get_csv_links(self, keywords, n_pages):

        my_list = []
        for word in keywords:
            for item in self.get_links(word, n_pages):
                if 'https://www.searchenginejournal.com/' in item:
                    my_list.append(item)

        self.create_csv('links.csv', my_list)
            

class GoogleStatsScraper(GoogleScraper):
    
    def get_stats(self, word):
    
        response = self.session.get("https://www.google.com//search?q=site:https://www.searchenginejournal.com/" + ' ' + word)
        results = response.html.find(self.css_id_result)

        for result in results:
            text = result.find(self.css_id_target, first=True).text
            clean_text = unicodedata.normalize("NFKD", text)
            pattern = re.search(r"\s\d+", clean_text)
            if pattern != None:
                yield pattern.group()
            else:
                pattern = re.search(r"\s\d+\s\d+", clean_text)
                yield pattern.group()

            
            
    def get_csv_stats(self, keywords):
    
        my_list = []
        for word in keywords:
            for item in self.get_stats(word):
                my_list.append(' ' + word + ':' + item)

        self.create_csv('stats.csv', my_list)

obj1 = GoogleLinkScraper(HTMLSession(), ".tF2Cxc", ".yuRUbf a")
obj2 = GoogleStatsScraper(HTMLSession(),".main", "#result-stats")
keywords = obj1.get_data()
obj1.get_csv_links(keywords, 2)
obj2.get_csv_stats(keywords)     

