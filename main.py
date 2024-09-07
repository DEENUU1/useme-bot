import logging
from scraper import scrape_offers
from fastapi import FastAPI
from dotenv import load_dotenv
import os
from pydantic import BaseModel


load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

app = FastAPI(debug=DEBUG, docs_url="/docs" if DEBUG else None, redoc_url=None)


class ScrapeRequest(BaseModel):
    url: str


@app.post("/scraper")
def run_scraper_handler(data: ScrapeRequest):
    logger.info(f"Running scraper for {data.url}")
    offers = scrape_offers(data.url)
    return offers


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
