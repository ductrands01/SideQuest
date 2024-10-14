FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# EXPOSE 8080
COPY . /app
CMD ["tail", "-f", "/dev/null"]