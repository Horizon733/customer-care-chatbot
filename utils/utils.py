import logging
import mimetypes
import os
import smtplib
import traceback
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path

logger = logging.getLogger(__name__)


def send_email(subject:str, recipient_email:str, content:str):
    try:
        message_data = EmailMessage()
        message_data["Subject"] = subject
        username = os.environ["EMAIL"]
        password = os.environ["PASS"]
        message_data["From"] =username
        message_data["To"] = recipient_email
        image_cid = make_msgid(domain="xyz.com")
        message_data.add_alternative(content.format(image_cid=image_cid), subtype="html")
        this_path = Path(os.path.realpath(__file__))
        image_data, maintype, subtype = get_image_data(f"{this_path.parent}/assets/img/email.png")
        message_data.get_payload()[0].add_related(
            image_data,
            maintype=maintype,
            subtype=subtype,
            image_cid=image_cid
        )
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp_server:
            smtp_server.login(username, password)
            smtp_server.send_message(message_data)
        return True
    except Exception as error:
        logger.error(f"Error: {error}")
        logger.info(traceback.print_exc())
        return False


def get_image_data(filepath:str):
    with open(filepath, "rb") as image_data:
        maintype, subtype = mimetypes.guess_type(image_data.name)[0].split("/")
        return image_data.read(), maintype, subtype


def get_html_data(filepath:str):
    with open(filepath, "r") as html_data:
        return html_data.read()