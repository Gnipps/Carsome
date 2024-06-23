# Carsome Interview Test

## Section A: SQL
The anwers for the SQL questions are in the file `SQL.sql`

## Section B: Web Scraping

The web scraping code is in the file `web_scrape.py`
dockerfile is in the file `Dockerfile`

To run the code, you can use the following command:

```
docker pull gnipps/carsome-web-scrape:latest
```
```
docker build -t carsome-web-scrape:latest .
```
```
docker run carsome-web-scrape:lastest
```
web_scrape.py will be executed in the docker container and the output will be saved as `car_data.csv`
> Note: python3 web_scrape.py is expected to return error as the code is written to run in the docker container

The output will be saved as `car_data.csv`

The image is also available in the [docker hub link](https://hub.docker.com/repository/docker/gnipps/carsome-web-scrape/)


## Section C: Data Ingestion pipeline

The answer for the Data Ingestion pipeline questions is in the file `Carsome Q3.docx`
