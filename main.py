import logging
from scraper import scrape
logger = logging.getLogger(__name__)



def main():
    urls = [""]

    for url in urls:
        offers = scrape(url)
        # TODO sand offers by email
        logger.info(f"Found {len(offers)} offers")


if __name__ == '__main__':
    main()
