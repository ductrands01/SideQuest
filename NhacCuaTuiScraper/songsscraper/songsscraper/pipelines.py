# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class SongsscraperPipeline:
    def process_item(self, item, spider):
        return item


import mysql.connector
import os

class MySQLPipeline:
    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'scrapy_user'),
            password=os.getenv('MYSQL_PASSWORD', 'password'),
            database=os.getenv('MYSQL_DATABASE', 'songs_db')
        )
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO songs (category_name, category_url, song_name, song_url, author, lyrics, tags, poster, image, audio_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            item['category_name'], item['category_url'], item['song_name'],
            item['song_url'], item['author'], item['lyrics'],
            ','.join(item['tags']), item['poster'], item['image'],
            item['audio_url']
        ))
        return item
