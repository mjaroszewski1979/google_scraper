
# Importing required libraries
import urllib
from requests_html import HTML
from requests_html import HTMLSession
import csv
import unicodedata


# Creating parent class which includes few attributes and methods shared between subclasses
class GoogleScraper:
    def __init__(self, session, css_id_result, css_id_target):
        self.session = session
        self.css_id_result = css_id_result
        self.css_id_target = css_id_target
        
    # Function for opening file using context manager
    def get_data(self):

        with open('keywords.txt') as f:
            keywords = f.read()   
            keywords = keywords.split(', ')

        return keywords
    
    # This function is used to create a writer object and to write single rows to the CSV file 
    def create_csv(self, file_name, list_name):
        
        with open(file_name, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(list_name)
        
# Creating a subclass which inherits from GoogleScraper             
class GoogleLinkScraper(GoogleScraper):
    
    # This function accepts one of the keywords as well as number of pages on the google search results
    def get_links(self, word, n_pages):
        for page in range(1, n_pages):
            
            # Creating a response object
            response = self.session.get("http://www.google.com/search?q=site:https://www.searchenginejournal.com/" + ' ' + word + "&start=" + str((page - 1) * 10))
            
            # Using provided css identifier to to retrieve desired element 
            results = response.html.find(self.css_id_result)
            
            # Looping thru all the results to yield a link destination
            for result in results:
                yield result.find(self.css_id_target, first=True).attrs['href']

    # Function to create a csv file with list of links containing phrase 'https://www.searchenginejournal.com/'
    def get_csv_links(self, keywords, n_pages):

        my_list = []
        for word in keywords:
            for item in self.get_links(word, n_pages):
                if 'https://www.searchenginejournal.com/' in item:
                    my_list.append(item)

        self.create_csv('links.csv', my_list)
            
# Creating a subclass which inherits from GoogleScraper
class GoogleStatsScraper(GoogleScraper):

    # This function accepts one of the keywords and yields number of search results
    def get_stats(self, word):
    
        # Creating a response object
        response = self.session.get("https://www.google.com//search?q=site:https://www.searchenginejournal.com/" + ' ' + word )
        
        # Using provided css identifier to to retrieve desired element 
        results = response.html.find(self.css_id_result)

        # Looping thru all the results to yield a number of search results
        for result in results:
            try:
                text = result.find(self.css_id_target, first=True).text
                
                # Cleaning up text data
                clean_text = unicodedata.normalize("NFKD", text)
                yield clean_text[:-9]
            except AttributeError:
                pass
            
    # Function to create a csv file with number of search results and the associated keyword   
    def get_csv_stats(self, keywords):
    
        my_list = []
        for word in keywords:
            for item in self.get_stats(word):
                my_list.append(' ' + word + ':' + ' ' + item)

        self.create_csv('stats.csv', my_list)

# Creating objects and passing as arguments names of the css identifiers obtained using chrome developer tools       
obj1 = GoogleLinkScraper(HTMLSession(), ".tF2Cxc", ".yuRUbf a")
obj2 = GoogleStatsScraper(HTMLSession(),".main", "#result-stats")

# Fetching keywords from 'keywords.txt' file present in project root folder
keywords = obj1.get_data()

# Calling methods to create seperate csv files
obj1.get_csv_links(keywords, 2)
obj2.get_csv_stats(keywords)     


