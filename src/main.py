import requests
from requests import Response
import json
import sys
import os

from bs4 import BeautifulSoup
from typing import Final
from enum import Enum
from datetime import datetime

URL: Final[str] = "https://yasno.com.ua/b2c-tariffs"
HEADERS: Final[dict] = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
}
DIV: Final[str] = "partial-tariff-price"


class JSONHandler():
    def __init__(self, filename: str) -> None:
        self._filename: str = filename

    @property
    def is_empty(self) -> bool:
        return not os.path.exists(self._filename) \
                or os.path.getsize(self._filename) == 0

    def read(self) -> any:
        with open(self._filename, "r") as f:
            loaded_data: any = json.load(f)

        return loaded_data

    def write(self, data: any) -> None:
        with open(self._filename, "w") as f:
            json.dump(data, f, indent=4)


class PriceParser():
    def __init__(self, url: str, headers: dict) -> None:
        self._url: str = url
        self._headers: dict = headers
        self._response: Response = self._get_response()
        self._html: str = self._response.text
        self._soup = BeautifulSoup(self._html, "html.parser")
        self._price: float = self._get_price_from_page()

    @property
    def price(self) -> float:
        return self._price

    def _get_response(self) -> Response:
        try:
            r: Response = requests.get(
                self._url, headers=self._headers, timeout=10)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def _get_price_from_page(self) -> float:
        blocks = self._soup.find_all("div", class_=DIV)

        for block in blocks:
            title = block.find("h3", class_=f"{DIV}__title")
            if title and title.text.strip() == "з ПДВ":
                price = block.find("strong", class_=f"{DIV}__value")
                if price:
                    return float(price.text.replace(",", "."))


class ElectricityTariff():
    def __init__(self, parser: PriceParser) -> None:
        self._parser: PriceParser = parser
        self._prices: dict = self._get_tariff()
        self._hour = datetime.now().hour

    def _get_tariff(self) -> dict:
        return {
            "day": self._parser.price,
            "night": self._parser.price / 2,
        }

    @property
    def prices(self) -> dict:
        return self._prices


def main() -> None:
    parser: PriceParser = PriceParser(URL, HEADERS)
    tariff: ElectricityTariff = ElectricityTariff(parser)
    hour = datetime.now().hour
    print(tariff.prices["night"] if hour <= 7 and hour > 23 else tariff.prices["day"])


if __name__ == "__main__":
    main()
