FROM python:3.10.13

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app/sreality_scraper
CMD ["bash", "-c", "scrapy crawl scrapme && python /app/app.py"]