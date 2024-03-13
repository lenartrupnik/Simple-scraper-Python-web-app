import json
import scrapy
import logging
from sreality_scraper.items import SrealityItem
from urllib.parse import urlencode


class ScrapmeSpider(scrapy.Spider):
    """
    A Scrapy spider for scraping real estate data from the Sreality API.

    Attributes:
        name (str): The name of the spider.
        api_url (str): The base URL of the Sreality API.
        params (dict): Parameters for the API request.
    """

    name = "scrapme"
    api_url = "https://www.sreality.cz/api/cs/v2/estates?"
    params = {'category_main_cb': '1',
              'category_type_cb': '1',
              'page': 1,
              'per_page': 20
              }

    item_counter = 0

    def start_requests(self):
        """ Generates a Scrapy FormRequest to initiate the scraping process. """
        self.log("Starting the scraper ...")
        yield scrapy.FormRequest(url=self.build_url(),
                                 callback=self.parse_api_response)

    def parse_api_response(self, response):
        """
        Parses the API response and extracts estate data. It yields SrealityItem objects.

        Args:
            response (scrapy.http.Response): The response from the API request.
        """
        try:
            response_data = json.loads(response.text)

            for estate in response_data['_embedded']['estates']:
                sreality_item = SrealityItem()
                sreality_item['title'] = estate['name']
                sreality_item['image_url'] = estate['_links']['images'][0]['href']
                self.item_counter += 1
                yield sreality_item

            new_page = response_data['page'] + 1

            if new_page <= 25:
                self.params["page"] = new_page
                yield response.follow(url=self.build_url(),
                                    callback=self.parse_api_response,
                                    body=json.dumps(self.params))
                
        except Exception as e:
            logging.error("Error parsing API response: {e}")

    def build_url(self):
        """
        Builds the URL for the API request using the specified parameters.

        Returns:
            str: The URL string for the API request.
        """
        return self.api_url + urlencode(self.params)
