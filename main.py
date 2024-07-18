import logging
import logging.handlers
import os

import requests

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)
h = 0
try:
    SOME_SECRET = os.environ["SOME_SECRET"]
    CK = os.environ["CK"]
    CS = os.environ["CS"]
    PRODUCT_URL = os.environ["PRODUCT_URL"]
    BATCH_PRODUCT_URL = os.environ["BATCH_PRODUCT_URL"]
    MY_GMAIL = os.environ["MY_GMAIL"]
except KeyError:
    SOME_SECRET = "Token not available!"
    CK = "Token not available!"
    CS = "Token not available!"
    BATCH_PRODUCT_URL = "Token not available!"
    MY_GMAIL = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")
    logger.info(f"Token value: {CK}")
    logger.info(f"Token value: {PRODUCT_URL}")
    logger.info(f"Token value: {BATCH_PRODUCT_URL}")

    r = requests.get('https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE')
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f'Weather in Berlin: {temperature}')