import requests
from bs4 import BeautifulSoup
import logging
from dataclasses import dataclass
from typing import List, Optional
from history import LocalVisitedOffers

logger = logging.getLogger(__name__)


@dataclass
class Offer:
    url: Optional[str] = None
    category: Optional[str] = None
    title: Optional[str] = None


def get_page_content(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.exceptions.HTTPError as e:
        logger.error(e)
    except requests.exceptions.RequestException as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)


def parse_page(content: str) -> List[Optional[Offer]]:
    offer_history = LocalVisitedOffers()

    soup = BeautifulSoup(content, "html.parser")
    offers = []

    raw_offers = soup.find_all("article", class_="job")
    logger.info(f"Found {len(raw_offers)} offers")

    for offer_tag in raw_offers:
        title_url = offer_tag.find("a", class_="job__title")

        offer = Offer(
            url=f"https://useme.com{title_url.get("href")}",
            title=title_url.text.strip() if title_url.text else "",
        )

        if offer_history.check_if_url_exist(offer.url):
            logger.info(f"Offer {offer.url} already exists in history")
            continue
        else:
            offer_history.add_url_to_file(offer.url)

        offers.append(offer)

    logger.info(f"Parsed {len(offers)} offers")
    return offers


def scrape_offers(url: str) -> List[Offer]:
    page_content = get_page_content(url)
    offers = parse_page(page_content)
    return offers
