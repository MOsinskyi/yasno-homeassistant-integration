import logging
from typing import Final

import requests
from bs4 import BeautifulSoup
from requests import Response

logging.basicConfig(level=logging.DEBUG, filename="priceparser.log", filemode="w")

URL: Final[str] = "https://yasno.com.ua/b2c-tariffs"
HEADERS: Final[dict] = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1)\
                    AppleWebKit/605.1.15 (KHTML, like Gecko) \
                    Version/15.4 Safari/605.1.15",
}
DIV: Final[str] = "partial-tariff-price"


class PriceParser:
    def __init__(self) -> None:
        self.__url = URL
        self.__headers = HEADERS
        self.__response = self.__get_response()
        self.__soup = BeautifulSoup(self.__response.text, "html.parser")
        self.__price = self.__get_price_from_page()

    @property
    def price(self) -> float:
        return self.__price

    def __get_response(self) -> Response:
        response = None

        try:
            response = requests.get(self.__url, headers=self.__headers, timeout=10)
        except requests.exceptions.RequestException as e:
            logging.error(e)

        logging.info(response.raise_for_status())
        return response

    def __get_price_from_page(self) -> float:
        return_price = .0

        blocks = self.__soup.find_all("div", class_=DIV)

        for block in blocks:
            title = block.find("h3", class_=f"{DIV}__title")
            if title and title.text.strip() == "з ПДВ":
                price = block.find("strong", class_=f"{DIV}__value")
                if price:
                    return_price = float(price.text.replace(",", "."))

        return return_price
