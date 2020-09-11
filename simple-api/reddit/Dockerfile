FROM python:3

WORKDIR /usr/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "scraper.py"]