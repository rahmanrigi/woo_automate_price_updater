import logging
import logging.handlers
import os

import base64
from bs4 import BeautifulSoup
import smtplib
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

try:
    CONSUMER_KEY = os.environ["CONSUMER_KEY"]
    CONSUMER_SECRET = os.environ["CONSUMER_SECRET"]
    URL = os.environ["URL"]
    BATCH_PRODUCTS_UPDATE_URL = os.environ["BATCH_PRODUCTS_UPDATE_URL"]
    EMAIL = os.environ["EMAIL"]
    EMAIL_APP_PASSWORD = os.environ["EMAIL_APP_PASSWORD"]
    RECEIVE_EMAIL = os.environ["RECEIVE_EMAIL"]
    CURRENCY_URL = os.environ["CURRENCY_URL"]
except KeyError:
    SOME_SECRET = "Token not available!"
    CONSUMER_KEY = "Token not available!"
    CONSUMER_SECRET = "Token not available!"
    URL = "Token not available!"
    EMAIL = "Token not available!"
    EMAIL_APP_PASSWORD = "Token not available!"
    RECEIVE_EMAIL = "Token not available!"
    CURRENCY_URL = "Token not available!"
    #logger.info("Token not available!")
    #raise

# create authorization header
credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
base64_credentials = base64.b64encode(credentials.encode("utf-8")).decode("utf-8")
headers = {
    "Authorization": f"Basic {base64_credentials}",
    "User-Agent": "My User Agent"  # replace with a valid user agent string
}

param = {
    "per_page": 100
}
try:
    response = requests.get(url=URL, headers=headers, params=param)
    response.raise_for_status()
    products = response.json()
except Exception as error:
    logger.info(f"unsuccessful request: {error}")
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=EMAIL, password=EMAIL_APP_PASSWORD)
        connection.sendmail(from_addr=EMAIL,
                        to_addrs=f"{RECEIVE_EMAIL}",
                        msg=f"Subject:Woo Price update failed\n\nAccess to the products was fail. So, products price update failed. Error message: {error}")



def price_finder():
    global dollar_price, pond_price, euro_price, try_turkey_price, aed_emirates_price, CURRENCY_URL
    url = CURRENCY_URL
    try:
        currencyـheaders = {
            "Accept-Language" : "en-US,en;q=0.5",
            "User-Agent": "Defined",
        }
        page = requests.get(url, headers=currencyـheaders)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as error:
        logger.info(f"unsuccessful request: {error}")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=EMAIL, password=EMAIL_APP_PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=f"{RECEIVE_EMAIL}",
                                msg=f"Subject:Woo Price update failed\n\nconnection to {url} wasn't successful. So, products price update failed. Error message: {error}")


    usd_max = soup.find(id="usdmax")
    dollar = usd_max.text.replace(",", "")
    dollar_price = int(str(dollar)[:-1])

    en_pond = soup.find(id="price_gbp")
    pond = en_pond.text.replace(",", "")
    pond_price = int(str(pond)[:-1])

    eur = soup.find(id="price_eur")
    eur = eur.text.replace(",", "")
    euro_price = int(str(eur)[:-1])
    
    aed_emirates = soup.find(id="price_aed")
    aed = aed_emirates.text.replace(",", "")
    aed_emirates_price = int(str(aed)[:-1])
    
    try_turkey = soup.find(id="price_try")
    try_tr = try_turkey.text.replace(",", "")
    try_turkey_price = int(str(try_tr)[:-1])

price_finder()

data = {'update': []
        }

def calculate_prices(price,value, p_id):
    global data, rounded_product_today_price

    product_today_price = (price * value) + 100000
    rounded_product_today_price = round(product_today_price, -4)

    product_price_data = {'id': p_id,
                    'regular_price': rounded_product_today_price}

    data["update"].append(product_price_data)
        
for product in products:
    product_name = product['name']
    product_id = product['id']
    product_yesterday_price = product['price']
    product_attributes = product['attributes']
    for attribute in product_attributes:
        if attribute['id'] == 5:
            currency_type = attribute['options'][0]
        if attribute['id'] == 3:
            product_value = int(attribute['options'][0])
    if currency_type == "DOLLAR":
        calculate_prices(dollar_price,product_value,product_id)
    if currency_type == "TRY":
        calculate_prices(try_turkey_price, product_value, product_id)
    if currency_type == "AED":
        calculate_prices(aed_emirates_price, product_value, product_id)
    if currency_type == "EURO":
        calculate_prices(euro_price, product_value, product_id)
    if currency_type == "POUND":
        calculate_prices(pond_price, product_value, product_id)


if __name__ == "__main__":
    # logger.info(f"Token value: {SOME_SECRET}")        
    try:
        woo_response = requests.post(BATCH_PRODUCTS_UPDATE_URL, headers=headers, json=data)
        if woo_response.status_code == 200:
            with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=EMAIL_APP_PASSWORD)
                connection.sendmail(from_addr=EMAIL,
                                    to_addrs=f"{RECEIVE_EMAIL}",
                                    msg=f"Subject:Products updated\n\n Congratulation! All products price updated successfully. connection to woocommerce was Ok!")
            # print("all products prices update was success.")
            logger.info(f'Everything is Ok!')
    except:
        with smtplib.SMTP("smtp.gmail.com") as connection:
                connection.starttls()
                connection.login(user=EMAIL, password=EMAIL_APP_PASSWORD)
                connection.sendmail(from_addr=EMAIL,
                                    to_addrs=f"{RECEIVE_EMAIL}",
                                    msg=f"Subject:update failed\n\n There is something wrong with woocommerce connection. All products price updated *wasn't* successfully")