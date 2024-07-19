import logging
import logging.handlers
import os
import requests
import base64
from bs4 import BeautifulSoup
import smtplib

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
h = 2

try:
    SOME_SECRET = os.environ["SOME_SECRET"]
    BERLIN = os.environ["BERLIN"]
except KeyError:
    SOME_SECRET = "Token not available!"
    BERLIN = "Token not available!"
    #logger.info("Token not available!")
    #raise


if __name__ == "__main__":
    logger.info(f"Token value: {SOME_SECRET}")

    r = requests.get(BERLIN)
    if r.status_code == 200:
        data = r.json()
        temperature = data["forecast"]["temp"]
        logger.info(f'Weather in Berlin: {temperature}')
        

# try:
#     SOME_SECRET = os.environ["SOME_SECRET"]
#     CK = os.environ["CK"]
#     CS = os.environ["CS"]
#     PRODUCT_URL = os.environ["PRODUCT_URL"]
#     BATCH_PRODUCT_URL = os.environ["BATCH_PRODUCT_URL"]
#     MY_GMAIL = os.environ["MY_GMAIL"]
#     MY_GMAIL_APP_PASS = os.environ["MY_GMAIL_APP_PASS"]
#     RECEIVE_GMAIL = os.environ["RECEIVE_GMAIL"]
#     PRICE_TARGET_URL = os.environ["PRICE_TARGET_URL"]
# except KeyError:
#     SOME_SECRET = "Token not available!"
#     CK = "Token not available!"
#     CS = "Token not available!"
#     PRODUCT_URL = "Token not available!"
#     BATCH_PRODUCT_URL = "Token not available!"
#     MY_GMAIL = "Token not available!"
#     MY_GMAIL_APP_PASS = "Token not available!"
#     RECEIVE_GMAIL = "Token not available!"
#     PRICE_TARGET_URL = "Token not available!"
#     #logger.info("Token not available!")
#     #raise

# # create authorization header
# credentials = f"{CK}:{CS}"
# base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
# headers = {
#     "Authorization": f"Basic {base64_credentials}",
#     "User-Agent": "My User Agent"  # replace with a valid user agent string
# }

# param = {
#     "per_page": 100
# }

# try:
#     response = requests.get(url=PRODUCT_URL, headers=headers, params=param)
#     response.raise_for_status()
#     products = response.json()
# except Exception as error:
#     with smtplib.SMTP("smtp.gmail.com") as connection:
#         connection.starttls()
#         connection.login(user=MY_GMAIL, password=MY_GMAIL_APP_PASS)
#         connection.sendmail(from_addr=MY_GMAIL,
#                         to_addrs=f"{RECEIVE_GMAIL}",
#                         msg=f"Subject:Woo Price update failed\n\nAccess to the products was fail. So, products price update failed. Error message: {error}")


# if __name__ == "__main__":
#     logger.info(f"Token value: {SOME_SECRET}")
#     logger.info(f"Token value: {RECEIVE_GMAIL}")
#     logger.info(f"Token value: {PRODUCT_URL}")
#     logger.info(f"Token value: {BATCH_PRODUCT_URL}")
#     logger.info(f"Token value: {PRICE_TARGET_URL}")

#     r = requests.get('https://weather.talkpython.fm/api/weather/?city=Berlin&country=DE')
#     if r.status_code == 200:
#         data = r.json()
#         temperature = data["forecast"]["temp"]
#         logger.info(f'Weather in Berlin: {temperature}')