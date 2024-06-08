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
    description: Optional[str] = None
    author: Optional[str] = None


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
        category, author, description = None, None, None

        title_url = offer_tag.find("a", class_="job__title")

        job_category = offer_tag.find("div", class_="job__category")
        if job_category:
            category = job_category.find("p")

        job_headline = offer_tag.find("div", class_="job__headline")
        if job_headline:
            author = job_headline.find("strong")

        content = offer_tag.find("div", class_="job__content")
        if content:
            description = content.find("p")

        offer = Offer(
            url=title_url.get("href"),
            title=title_url.text.strip() if title_url.text else "",
            category=category.text.strip() if category else "",
            author=author.text.strip() if author else "",
            description=description.text.strip() if description else "",
        )

        if offer_history.check_if_url_exist(offer.url):
            logger.info(f"Offer {offer.url} already exists in history")
            continue
        else:
            offer_history.add_url_to_file(offer.url)

        offers.append(offer)

    logger.info(f"Parsed {len(offers)} offers")
    return offers


def scrape(url: str) -> List[Offer]:
    page_content = get_page_content(url)
    offers = parse_page(page_content)
    return offers

