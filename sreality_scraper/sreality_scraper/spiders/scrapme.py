import scrapy
import json
from sreality_scraper.items import SrealityItem
from urllib.parse import urlencode

class ScrapmeSpider(scrapy.Spider):
    name = "scrapme"
    api_url = "https://www.sreality.cz/api/cs/v2/estates?"
    params = {'category_main_cb': '1',
                'category_type_cb': '1',
                'page': 1,
                'per_page': 20
                }
    
    def start_requests(self):
        yield scrapy.FormRequest(self.build_url(), callback=self.parse_api_response)
                
        
    def parse_api_response(self, response):
        response_data = json.loads(response.text)
        
        for estate in response_data['_embedded']['estates']:
            sreality_item = SrealityItem()
            sreality_item['title'] = estate['name']
            sreality_item['image_url'] = estate['_links']['images'][0]['href']
            yield sreality_item

        new_page = response_data['page'] + 1
        
        if new_page <= 20:
            self.params["page"] = new_page
            yield response.follow(self.build_url(), callback=self.parse_api_response, body=json.dumps(self.params))

    def build_url(self):
        return self.api_url + urlencode(self.params)
        
        
