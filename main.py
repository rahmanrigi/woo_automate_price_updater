import logging
import logging.handlers
import os
from giftcards import giftcards
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



def price_finder():
    global dollar_price, pond_price, euro_price, CURRENCY_URL
    
    try:
        currencyـheaders = {
            "Accept-Language" : "en-US,en;q=0.5",
            "User-Agent": "Defined",
        }
        page = requests.get(CURRENCY_URL, headers=currencyـheaders)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "html.parser")
    except Exception as error:
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()

            connection.login(user=EMAIL, password=EMAIL_APP_PASSWORD)
            connection.sendmail(from_addr=EMAIL,
                                to_addrs=f"{RECEIVE_EMAIL}",
                                msg=f"Subject:Woo Price update failed\n\nconnection to {CURRENCY_URL} wasn't successful. So, products price update failed. Error message: {error}")
         

    usd_max = soup.find(id="usdmax")
    eur = soup.find(id="price_eur")
    en_pond = soup.find(id="price_gbp")

    dollar = usd_max.text.replace(",", "")
    dollar_price = int(str(dollar)[:-1])

    pond = en_pond.text.replace(",", "")
    pond_price = int(str(pond)[:-1])

    eur = eur.text.replace(",", "")
    euro_price = int(str(eur)[:-1])

price_finder()



giftcards = giftcards

data = {'update': []
        }

def calculate_prices(money_price):
    global data
    gifts = ps_gifts[giftcards]
    
    for gift in gifts:
        card_value = gifts[gift]['value']

        card_price = (money_price * card_value) + 100000
        rounded_card_price = round(card_price, -4)

        # print(f"giftcard id: {gifts[gift]['id']}, giftcard value:{card_value}, card price: {card_price}")
        
        product_id = gifts[gift]['id']
        
        updated_data = {'id': product_id,
                        'regular_price': rounded_card_price}

        data["update"].append(updated_data)
        
ps_gifts = giftcards['playstation']

#Guide 
# update other tip of products like below and above
# it's for future more products 
# apple_gifts = giftcards['apple']
# and then add your condition like below
# finally call calculate_price() and pass
# related price on it

for giftcards in ps_gifts:
    if giftcards == "usa": 
        calculate_prices(dollar_price)     
    if giftcards == "emirates":
        calculate_prices(dollar_price)
    if giftcards == "england":
        calculate_prices(pond_price)
    if giftcards == "germany":
        calculate_prices(euro_price)


if __name__ == "__main__":
    # logger.info(f"Token value: {SOME_SECRET}")        
    try:
        woo_response = requests.post(BATCH_PRODUCTS_UPDATE_URL, headers=headers, json= data)
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