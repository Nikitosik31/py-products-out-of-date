import datetime
from unittest.mock import patch, MagicMock
import pytest
from app.main import outdated_products


real_date = datetime.date


def make_product(name: str, date: datetime.date, price: int = 100) -> dict:
    return {
        "name": name,
        "expiration_date": date,
        "price": price
    }


@pytest.mark.parametrize(
    "products, today, expected",
    [
        (
            [
                make_product("salom", datetime.date(2022, 2, 10)),
                make_product("chicken", datetime.date(2022, 1, 5)),
                make_product("duck", datetime.date(2022, 2, 1))
            ],
            datetime.date(2022, 2, 10),
            ["chicken", "duck"]
        ),
        (
            [
                make_product("salmon", datetime.date(2022, 2, 11)),
                make_product("chicken", datetime.date(2022, 2, 12))
            ],
            datetime.date(2022, 2, 10),
            []
        ),
        (
            [
                make_product("salmon", datetime.date(2022, 2, 10)),
            ],
            datetime.date(2022, 2, 10),
            []
        ),
        (
            [
                make_product("chicken", datetime.date(2022, 2, 9)),  # вчера
            ],
            datetime.date(2022, 2, 10),
            ["chicken"]
        )
    ]
)
@patch("app.main.datetime.date")
def test_outdated_products(
        mock_date: MagicMock,
        products: list,
        today: datetime.date,
        expected: list[str]
) -> None:
    mock_date.today.return_value = today
    mock_date.side_effect = lambda *args, **kwargs: real_date(*args, **kwargs)
    assert outdated_products(products) == expected
