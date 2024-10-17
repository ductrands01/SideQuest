# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import re


class NhaccuatuiScraperPipeline:
    def process_item(self, item, spider):
        if 'lyrics' in item:
            lyrics_raw = ''.join(item['lyrics'])
            lyrics_cleaned = re.sub(r'<[^>]+>', '', lyrics_raw)
            lyrics_cleaned = re.sub(r'\s+', ' ', lyrics_cleaned).strip()
            lyrics_cleaned = lyrics_cleaned.replace('\n', ' ').replace('\r', '').strip()
            item['lyrics'] = lyrics_cleaned
        return item


import pymysql
import logging

class MySQLPipeline:
    def open_spider(self, spider):
        """
        Called when the spider opens.
        This connects to the MySQL database.
        """
        self.connection = pymysql.connect(
            host=spider.settings.get('MYSQL_HOST'),
            user=spider.settings.get('MYSQL_USER'),
            password=spider.settings.get('MYSQL_PASSWORD'),
            db=spider.settings.get('MYSQL_DATABASE'),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
        self.cursor = self.connection.cursor()
        self.create_table()

    def close_spider(self, spider):
        """
        Called when the spider closes.
        This closes the MySQL connection.
        """
        self.connection.close()

    def create_table(self):
        """
        Create the `songs` table if it does not exist.
        """
        create_table_query = """
        CREATE TABLE IF NOT EXISTS songs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            url TEXT,
            name VARCHAR(255),
            authors TEXT,
            lyrics TEXT,
            poster TEXT,
            poster_url TEXT,
            category_name VARCHAR(255),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        ) CHARSET=utf8mb4;
        """
        self.cursor.execute(create_table_query)
        self.connection.commit()

    def process_item(self, item, spider):
        """
        Called for each item scraped by the spider.
        Inserts the item data into the MySQL database.
        """
        try:
            insert_query = """
            INSERT INTO songs (url, name, authors, lyrics, poster, poster_url, category_name)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (
                item.get('url'),
                item.get('name'),
                ', '.join(item.get('authors', [])),
                item.get('lyrics'),
                item.get('poster'),
                item.get('poster_url'),
                item.get('category_name')
            ))
            self.connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"Error inserting item into MySQL: {e}")
            self.connection.rollback()

        return item