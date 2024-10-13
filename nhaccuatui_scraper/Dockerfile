FROM python:3.9-slim

WORKDIR /app

RUN pip install scrapy pymysql python-dotenv google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2

COPY . /app

CMD ["/bin/bash"]
