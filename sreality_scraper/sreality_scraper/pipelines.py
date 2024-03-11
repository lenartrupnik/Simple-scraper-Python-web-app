# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2


class SrealityScraperPipeline:
    
    def __init__(self):
        try:
            # Connect to PostgreSQL database
            self.connection = psycopg2.connect(dbname = 'scrapy_db',
                                               host='db',
                                               user = 'postgres',
                                               password = '1Q2W3E4r!',
                                               port = "5432")
            
            self.cur = self.connection.cursor()
                        
            # Print PostgreSQL server version
            self.cur.execute("SELECT version();")
            record = self.cur.fetchone()
            print("You are connected to - ", record, "\n")
            
            self.cur.execute("""
            CREATE TABLE IF NOT EXISTS items(
                id serial PRIMARY KEY,
                title TEXT,
                image_url TEXT
            )""")
            
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            
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
            self.connection.commit()
        return item
    
    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()
