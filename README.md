## <img src="https://github.com/mjaroszewski1979/mjaroszewski1979/blob/main/brain.png">  &nbsp; Google Scraper
### This is a Python program powered by requests-HTML library to provide an efficient way to parsing HTML documents using CSS Selectors. Its main function is to query Google.com using the following set of queries: web address {keyword}. The main risk associated with using such a program is getting blocked while scraping by sending repetitive requests from the same IP. To avoid this, future improvements can be made, for example by using rotating proxies. A rotating proxy is a proxy server that allocates a new IP address from a set of proxies stored in the proxy pool. The purpose behind using the concept of rotating IPs is to make it look that you’re not a bot but a human, accessing data from different locations from different parts of the world. When we scrape data using an automated scraper, the scraper scrapes the data at an inhuman speed which is easily detected by anti-scrapers plugins. By adding random delays and actions to our scraper we can make it resemble a human, so the website owners don’t detect it. Logging into the same website at different day times also reduces your footprint.
--------------------------------------------------

### Installation Guide:
* Copy all the files from the repository - file 'keywords.txt' must be present in the project root folder
* Run pip install -r requirements.txt

--------------------------------------------------
