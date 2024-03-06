import requests
from bs4 import BeautifulSoup
import json

class DetailsScraper:
    def __init__(self, url):
        self.url = url

    def fetch_page(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            return None

    def extract_data(self, html):
        data = {}
        soup = BeautifulSoup(html, 'html.parser')

        # Extract company name
        company_name = soup.find('h2').text.strip()
        data['name'] = company_name

        # Extract details from table
        table = soup.find('table', class_='table-condensed')
        if table:
            rows = table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) == 2:
                    key = cols[0].text.strip()
                    value = cols[1].text.strip()
                    data[key] = value

        # # Extract details from "Contact Us" section
        # contact_section = soup.find('div', class_='listing-desc')
        # if contact_section:
        #     contact_info = contact_section.find_all('span')
        #     for info in contact_info:
        #         text = info.get_text(separator=' ').strip()
        #         if 'Mobile no' in text:
        #             data['mobile'] = text.split(':')[1].strip()
        #         elif 'Phone no' in text:
        #             data['phone'] = text.split(':')[1].strip()
        #         elif 'Address' in text:
        #             data['location'] = text.split(':')[1].strip()
        #         elif 'Website' in text:
        #             data['website'] = text.split(':')[1].strip()
        #         elif 'Email' in text:
        #             data['email'] = text.split(':')[1].strip()

        return data

    def scrape(self):
        page_content = self.fetch_page()
        if page_content:
            data = self.extract_data(page_content)
            return json.dumps(data, indent=4)
        else:
            print("Failed to fetch page.")
            return {}


# #-------------------------------------------------------
# #  ?            Example Usage
# url_to_scrape = 'https://www.2merkato.com/directory/40989-ledcon-manufacturing'
# scraper = DetailsScraper(url_to_scrape)
# scraped_data = scraper.scrape()
# print(scraped_data)
# #-------------------------------------------------------
