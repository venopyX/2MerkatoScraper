from DirectoryScraper import DirectoryScraper
from DetailsScraper import DetailsScraper
import json
import time

def get_urls_from_json(json_data):
    data = json.loads(json_data)
    urls = []
    for item in data:
        urls.append(item['url'])
    
    return urls

class CombinedScraper:
    def __init__(self):
        self.directory_scraper = DirectoryScraper()

    def scrape_combined_data(self, directory_url):
        directory_data_json = self.directory_scraper.scrape_directory(directory_url)
        directory_urls = get_urls_from_json(directory_data_json)
        combined_data = {"allbusinesses": []}  
        for url in directory_urls:
            print("Scraping:", url)  
            details_scraper = DetailsScraper(url)  
            details = details_scraper.scrape()
            if details is not None:  
                if isinstance(details, str):  
                    
                    details = details.replace('\n', '').replace('\r', '')  
                    combined_data["allbusinesses"].append({
                        "name": url,  
                        "details": json.loads(details)  
                    })
                else:
                    combined_data["allbusinesses"].append({
                        "name": url,  
                        "details": details
                    })
            else:
                combined_data["allbusinesses"].append({
                    "name": url,  
                    "details": {"Details not available"}  
                })
            time.sleep(2)  
        return json.dumps(combined_data, indent=4)


#-------------------------------------------------------
#  ?            Example Usage
if __name__ == "__main__":
    directory_url = "https://www.2merkato.com/directory/page:2"
    combined_scraper = CombinedScraper()
    combined_data = combined_scraper.scrape_combined_data(directory_url)
    print("Combined Data:", combined_data)
#-------------------------------------------------------