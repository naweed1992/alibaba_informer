import logging
from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    mail_user: str = environ.get("mail_user")
    mail_pass: str = environ.get("mail_pass")
