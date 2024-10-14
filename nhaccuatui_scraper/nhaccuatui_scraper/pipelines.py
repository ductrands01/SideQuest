# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class NhaccuatuiScraperPipeline:
    def process_item(self, item, spider):
        if 'lyrics' in item:
            lyrics_cleaned = [element.strip() for element in item['lyrics'] if isinstance(element, str)]
            item['lyrics'] = '\n'.join(lyrics_cleaned).strip()
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
            charset='utf8mb4',  # Supports extended characters
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
            category_name VARCHAR(255),
            category_url TEXT,
            song_url TEXT,
            title VARCHAR(255),
            authors TEXT,
            lyrics TEXT,
            poster TEXT,
            poster_url TEXT,
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
            INSERT INTO songs (category_name, category_url, song_url, title, authors, lyrics, poster, poster_url)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(insert_query, (
                item.get('category_name'),
                item.get('category_url'),
                item.get('song_url'),
                item.get('title'),
                ', '.join(item.get('authors', [])),
                item.get('lyrics'),
                item.get('poster'),
                item.get('poster_url')
            ))
            self.connection.commit()
        except pymysql.MySQLError as e:
            logging.error(f"Error inserting item into MySQL: {e}")
            self.connection.rollback()

        return item