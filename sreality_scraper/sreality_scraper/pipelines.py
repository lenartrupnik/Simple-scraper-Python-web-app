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
    
    def __init__(self):
        db_handler = DBHandler()
        self.cur = db_handler.get_cursor()
        self.conn = db_handler.get_conn()
                  
    def process_item(self, item, spider):
        #TODO: Better checking for duplicate data
        self.cur.execute("select * from items where title = %s", (item['title'],))
        result = self.cur.fetchone()
        
        if result:
            spider.logger.warn(f"Item already in database: {item['title']}" )
        
        else:
            self.cur.execute(""" insert into items (title, image_url) values (%s, %s)""", 
                            (item["title"],
                            item["image_url"]))
            self.conn.commit()
        return item
    
    def close_spider(self):
        self.cur.close()
