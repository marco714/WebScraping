# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
#Scraped Data -> Item Containers-> JSON/csv
#Scraped Data -> Item Containers -> Pipeline -> Sqlite/MongoDb

from itemadapter import ItemAdapter
import sqlite3

class QuotetutorialPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = sqlite3.connect("myquotes.db")
        self.cursor = self.conn.cursor()
        
    def create_table(self):
        self.cursor.execute("DROP TABLE IF EXISTS quotes_tb")
        self.cursor.execute("CREATE TABLE quotes_tb(title text, author text, tag text)")

    def process_item(self, item, spider):
        self.store_db(item)
        print(f"Pipeline :{item['title'][0]}")
        return item
    
    def store_db(self, item):
        self.cursor.execute("INSERT INTO quotes_tb VALUES(?,?,?)", (item['title'][0], item['author'][0], item['tags'][0]))
        self.conn.commit()
