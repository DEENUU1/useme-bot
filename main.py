import logging
from scraper import scrape

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    urls = ["https://useme.com/pl/jobs/category/programowanie-i-it,35/"]

    for url in urls:
        offers = scrape(url)
        # TODO sand offers by email
        logger.info(f"Found {len(offers)} offers")


if __name__ == '__main__':
    main()
