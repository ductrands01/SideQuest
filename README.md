# NhacCuaTui Scraper
---
A Scrapy project to scrape song and category information from the [NhacCuaTui](https://www.nhaccuatui.com/) website. The project extracts data like song names, authors, lyrics, and categories, saving them in a structured format for further use.

## Table of Contents

- [Project Structure](#project-structure)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Running the Category Spider](#running-the-category-spider)
  - [Running the Song Spider](#running-the-song-spider)
- [Configuration](#configuration)
- [Scraped Items](#scraped-items)
- [Middlewares](#middlewares)
- [Item Pipelines](#item-pipelines)
- [Data Scraped](#data-scraped)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Project Structure

```
nhaccuatui_scraper/
│
├── nhaccuatui_scraper/
│   ├── spiders/
│   │   ├── __init__.py
│   │   ├── nhaccuatui_categories.py   # Spider for scraping categories
│   │   └── nhaccuatui_songs.py        # Spider for scraping songs
│   │
│   ├── __init__.py
│   ├── items.py                       # Models for scraped data
│   ├── middlewares.py                 # Custom middlewares
│   ├── pipelines.py                   # Pipelines for processing scraped data
│   ├── settings.py                    # Scrapy settings configuration
│   └── scrapy.cfg                     # Scrapy project configuration
│
├── data/
│   ├── categories.csv                 # CSV of scraped categories
│   ├── songs.csv                      # CSV of scraped songs
│   └── nhaccuatui_db.sql              # SQL dump for database storage
│
├── requirements.txt                   # Python dependencies
├── README.md                          # Project documentation
└── .env                               # Environment variables

```

## Features

- **Category-Based Scraping**: Scrape categories (genres) and songs from NhacCuaTui.
- **Pagination Handling**: Automatically processes multiple pages within a category.
- **Data Cleaning**: Cleans song lyrics to remove HTML tags and unnecessary characters.
- **Storage Options**: Save data to CSV files or a MySQL database.
- **Customizable**: Configure settings, user-agents, and proxy settings to avoid blocking.

## Getting Started

### Prerequisites

Ensure you have Python installed. You can download Python from [python.org](https://www.python.org/downloads/). 

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/ductrands01/SideQuest
   cd SideQuest/nhaccuatui_scraper
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   - Create a `.env` file in the project root:
     ```env
     #SCRAPEOPS
     SCRAPEOPS_API_KEY="YOUR-API-KEYS"

     #MYSQL
     MYSQL_HOST=your_mysql_host
     MYSQL_DATABASE=your_database_name
     MYSQL_USER=your_mysql_user
     MYSQL_PASSWORD=your_mysql_password
     SCRAPEOPS_API_KEY=your_scrapeops_api_key
     ```

## Usage

### Running the Category Spider

The `NhaccuatuiCategoriesSpider` extracts categories from NhacCuaTui and saves them to `data/categories.csv`.

```bash
scrapy crawl nhaccuatui_categories
```

### Running the Song Spider

The `NhaccuatuiSongsSpider` scrapes songs based on URLs from the category spider or a specified category URL.

```bash
scrapy crawl nhaccuatui_songs
```

Customize the category URL directly in `settings.py` or pass it via the command line:
```bash
scrapy crawl nhaccuatui_songs -a category_url='https://www.nhaccuatui.com/bai-hat/rbhip-hoprap-moi.html'
```

## Configuration

Edit `settings.py` for configurations like user-agents, proxies, and export formats. 

- **Enable middlewares**:
  ```python
  DOWNLOADER_MIDDLEWARES = {
      "nhaccuatui_scraper.middlewares.ScrapeOpsFakeUserAgentMiddleware": 100,
      "nhaccuatui_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 200,
      "nhaccuatui_scraper.middlewares.ScrapeOpsProxyMiddleware": 300,
  }
  ```

- **Set MySQL connection details** in `.env`:
  ```env
  MYSQL_HOST=your_host
  MYSQL_DATABASE=your_db
  MYSQL_USER=your_user
  MYSQL_PASSWORD=your_password
  ```

## Scraped Items

### NhaccuatuiSong

| Field          | Description                                              |
|----------------|----------------------------------------------------------|
| `url`          | URL of the song's page                                   |
| `name`         | Title of the song                                        |
| `authors`      | List of authors/artists                                  |
| `lyrics`       | Cleaned lyrics                                           |
| `poster`       | Name of the person/entity who posted the song            |
| `poster_url`   | Profile URL of the poster                                |
| `category_name`| Category (genre)                                         |

### NhaccuatuiCategory

| Field   | Description                        |
|---------|------------------------------------|
| `url`   | URL of the category page           |
| `name`  | Name of the category (e.g., Pop)   |

## Middlewares

The project includes custom middlewares:
- **User-Agent Spoofing**: Randomly selects a user-agent to avoid detection.
- **Proxy Integration**: Routes requests through proxies.
- **Browser Headers**: Adds fake browser headers to make requests look legitimate.

Configure middlewares in `settings.py` and make sure your `.env` has the `SCRAPEOPS_API_KEY`.

## Item Pipelines

### NhaccuatuiScraperPipeline

Cleans song lyrics by removing HTML tags and extra whitespace.

### MySQLPipeline

Stores scraped song data into a MySQL database. Make sure your database credentials are correctly set up in `.env`.

Enable the pipelines in `settings.py`:
```python
ITEM_PIPELINES = {
    "nhaccuatui_scraper.pipelines.NhaccuatuiScraperPipeline": 300,
    'nhaccuatui_scraper.pipelines.MySQLPipeline': 400
}
```

## Data Scraped
Scraped data can be found in the nhaccuatui_scraper/data directory, including:

- **categories.csv**: Contains category (genre) information.
- **songs.csv**: Stores information about individual songs.
- **nhaccuatui_db.sql**: SQL file to recreate the database structure and data.

## Acknowledgments

- Thanks to [NhacCuaTui](https://www.nhaccuatui.com/) for providing the content.
- Built using [Scrapy](https://scrapy.org/).
- Proxy and User-Agent features powered by [ScrapeOps](https://scrapeops.io/).

