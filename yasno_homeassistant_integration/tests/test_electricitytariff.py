from yasno_homeassistant_integration.electricitytariff import ElectricityTariff
from yasno_homeassistant_integration.priceparser import PriceParser


def test_get_tariff(mocker) -> None:
    mock_price_parser = mocker.Mock(spec=PriceParser)

    mock_price_parser.price.return_value = 4.32

    electricity_tariff = ElectricityTariff(PriceParser())

    expected = {
        "first_zone": {
            "with_fee": 4.32,
        },
        "second_zone": {
            "day": 4.32,
            "night": 2.16,
        },
        "third_zone": {
            "peak": 6.48,
            "half_peak": 4.32,
            "night": 1.73,
        },
    }

    result = electricity_tariff.prices

    assert result == expected
