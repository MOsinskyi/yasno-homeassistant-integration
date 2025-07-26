from priceparser import PriceParser

class ElectricityTariff():
    def __init__(self, parser: PriceParser) -> None:
        self._parser = parser
        self._prices = self._get_tariff()

    def _get_tariff(self) -> dict:
        return {
            "first_zone": {
                "with_fee": self._parser.price,
            },
            "second_zone": {
                "day": self._parser.price,
                "night": round(self._parser.price / 2, 2),
            },
            "third_zone": {
                "peak": round(self._parser.price * 1.5, 2),
                "half_peak": self._parser.price,
                "night": round(self._parser.price / 2.5, 2),
            },
        }

    @property
    def prices(self) -> dict:
        return self._prices
        