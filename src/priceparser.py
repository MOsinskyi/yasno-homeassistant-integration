import requests

from typing import Final
from requests import Response
from bs4 import BeautifulSoup

URL: Final[str] = "https://yasno.com.ua/b2c-tariffs"
HEADERS: Final[dict] = {
    "Accept": "text/html",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1)\
                    AppleWebKit/605.1.15 (KHTML, like Gecko) \
                    Version/15.4 Safari/605.1.15",
}
DIV: Final[str] = "partial-tariff-price"


class PriceParser():
    def __init__(self) -> None:
        self._url = URL
        self._headers = HEADERS
        self._response = self._get_response()
        self._html = self._response.text
        self._soup = BeautifulSoup(self._html, "html.parser")
        self._price = self._get_prices_from_page()

    @property
    def price(self) -> float:
        return self._price

    def _get_response(self) -> Response:
        try:
            r = requests.get(
                self._url, headers=self._headers, timeout=10)
            r.raise_for_status()
            return r
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the page: {e}")
            return None

    def _get_prices_from_page(self) -> float:
        blocks = self._soup.find_all("div", class_=DIV)

        for block in blocks:
            title = block.find("h3", class_=f"{DIV}__title")
            if title and title.text.strip() == "з ПДВ":
                price = block.find("strong", class_=f"{DIV}__value")
                if price:
                    return float(price.text.replace(",", "."))
