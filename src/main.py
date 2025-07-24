import requests
from requests import Response
import json
import sys

from bs4 import BeautifulSoup
from typing import Final

URL: Final[str] = "https://yasno.com.ua/b2c-tariffs"


def get_response(url: str, headers: Final[dict]) -> Response | None:
    try:
        response: Response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the page: {e}", file=sys.stderr)
        return None


class ElectricityTariff():
    def __init__(self, url: str) -> None:
        self._url: str = url
        self._headers: Final[dict] = {
            "Accept": "text/html",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.4 Safari/605.1.15",
        }

        self._response: Response = get_response(self._url, self._headers)
        self._soup = BeautifulSoup(self._response.text, "html.parser")

        self._prices: dict | None = self._parse_prices()

    def _parse_prices(self) -> dict | None:
        title_element = self._soup.find("h3", class_="partial-tariff-price__title", string="з ПДВ")
        
        prices: dict = {}

        if title_element:
            parent_div = title_element.find_parent("div", class_="partial-tariff-price")

            if parent_div:
                price_element: any = self._soup.find("strong", class_="partial-tariff-price__value")

                if price_element:
                    try:
                        day_price_text: str = price_element.get_text(strip=True)
                        day_price_text = day_price_text.replace(",", ".")

                        day_price: float = float(day_price_text)
                        night_price: float = day_price / 2

                        prices["day_price"] = day_price
                        prices["night_price"] = night_price

                    except ValueError as e:
                        print(f"Error parsing day price from element '{day_price_text}': {e}", file=sys.stderr)
                        return None
                else:
                    print("Could not find the price value element within the 'з ПДВ' block.", file=sys.stderr)
                    return None
            else:
                print("Could not find the parent 'partial-tariff-price' div for 'з ПДВ' title.", file=sys.stderr)
                return None
        else:
            print("Could not find the 'з ПДВ' title element on the page.", file=sys.stderr)
            return None

        return prices

    @property
    def prices(self) -> dict:
        return self._prices


def main() -> None:
    tariff = ElectricityTariff(URL)

    print(json.dumps(tariff.prices)) if tariff else json.dumps({})

if __name__ == "__main__":
    main()
