import json

from priceparser import PriceParser
from electricitytariff import ElectricityTariff


def main() -> None:
    parser = PriceParser()
    tariff = ElectricityTariff(parser)
    print(json.dumps(tariff.prices, indent=4))


if __name__ == "__main__":
    main()
