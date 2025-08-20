from priceparser import PriceParser

class ElectricityTariff:
    def __init__(self, parser: PriceParser) -> None:
        self.__parser = parser
        self.__prices = self.__get_tariff()

    def __get_tariff(self) -> dict:
        return {
            "first_zone": {
                "with_fee": self.__parser.price,
            },
            "second_zone": {
                "day": self.__parser.price,
                "night": round(self.__parser.price / 2, 2),
            },
            "third_zone": {
                "peak": round(self.__parser.price * 1.5, 2),
                "half_peak": self.__parser.price,
                "night": round(self.__parser.price / 2.5, 2),
            },
        }

    @property
    def prices(self) -> dict:
        return self.__prices
        