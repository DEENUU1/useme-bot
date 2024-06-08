import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
from dotenv import load_dotenv
import os
import logging
from scraper import Offer
from typing import List, Optional


load_dotenv()

logger = logging.getLogger(__name__)

configuration = sib_api_v3_sdk.Configuration()
configuration.api_key['api-key'] = os.getenv('BREVO')
api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))

SENDER_EMAIL, SENDER_NAME = os.getenv('EMAIL_FROM'), os.getenv('EMAIL_FROM_NAME')
RECEIVER_EMAIL, RECEIVER_NAME = os.getenv('EMAIL_TO'), os.getenv('EMAIL_TO_NAME')


def offers_to_html(offers: List[Optional[Offer]]) -> str:
    if not offers:
        return "No offers"

    html_message = "<ul>"
    for offer in offers:
        html_message += f"<li> <a href='https://useme.com{offer.url}'>{offer.title}</a></li>"
    html_message += "</ul>"
    return html_message


def send_email(subject: str, offers: List[Offer]) -> None:
    sender = {"name": SENDER_EMAIL, "email": SENDER_EMAIL}
    to = [{"email": RECEIVER_EMAIL, "name": RECEIVER_NAME}]

    html_message = offers_to_html(offers)
    send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(
        to=to,
        html_content=html_message,
        sender=sender,
        subject=subject
    )

    try:
        api_instance.send_transac_email(send_smtp_email)
        logger.info(f"Email sent to {RECEIVER_EMAIL}")
        return
    except ApiException as e:
        logger.error(f"Email not sent to {RECEIVER_EMAIL}")
    except Exception as e:
        logger.error(f"Email not sent to {RECEIVER_EMAIL}")
