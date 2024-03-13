# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sys
sys.path.append('/app')
from database_utils.dbHandler import DBHandler


class SrealityScraperPipeline:
    """
    A Scrapy pipeline for processing items scraped by the Sreality spider.

    Attributes:
        cur (psycopg2.extensions.cursor): The database cursor.
        conn (psycopg2.extensions.connection): The database connection.
    """

    def __init__(self):
        """
        Initializes the pipeline by establishing a database connection and obtaining a cursor.
        """
        self.db_handler = DBHandler()
        self.cur = self.db_handler.get_cursor()
        self.conn = self.db_handler.get_conn()

    def process_item(self, item, spider):
        """
        Processes a scraped item by inserting it into the database.

        Args:
            item (scrapy.Item): The scraped item.
            spider (scrapy.Spider): The spider that scraped the item.

        Returns:
            scrapy.Item: The processed item.
        """
        # TODO: Check for duplicate data
        self.cur.execute(""" insert into items (title, image_url) values (%s, %s)""",
                            (item["title"],
                            item["image_url"]))
        self.conn.commit()
        
        return item
