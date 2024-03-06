import requests
from bs4 import BeautifulSoup
import json

class DirectoryScraper:
    base_url = 'https://www.2merkato.com'
    
    def fetch_html(self, url):
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            print(f"Failed to fetch HTML content from {url}.")
            return None
    
    def parse_html(self, html_content):
        if html_content:
            return BeautifulSoup(html_content, 'html.parser')
        else:
            return None
    
    def extract_information(self, soup):
        items = []
        if soup:
            listings = soup.find_all(class_="span12 listing-summary-featured")
            for listing in listings:
                name = listing.find("h4").find("a").text.strip()
                relative_url = listing.find("h4").find("a")["href"]
                full_url = self.base_url + relative_url
                items.append({"name": name, "url": full_url})
        return items

    
    def scrape_directory(self, directory_url):
        html_content = self.fetch_html(directory_url)
        soup = self.parse_html(html_content)
        if soup:
            information = self.extract_information(soup)
            return json.dumps(information, indent=4)
        else:
            return None

# #-------------------------------------------------------
# #  ?            Example Usage
# directory_url = "https://www.2merkato.com/directory/"
# scraper = DirectoryScraper()
# result = scraper.scrape_directory(directory_url)
# print(result)
# #-------------------------------------------------------
