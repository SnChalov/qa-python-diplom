from unittest.mock import Mock
import pytest
from praktikum.burger import Burger


@pytest.fixture
def burger():
    return Burger()


@pytest.fixture
def bun():
    bun = Mock()
    bun.get_name.return_value = "black bun"
    bun.get_price.return_value = 100
    return bun


@pytest.fixture
def ingredient():
    ingredient = Mock()
    ingredient.get_name.return_value = "hot sauce"
    ingredient.get_type.return_value = "SAUCE"
    ingredient.get_price.return_value = 50
    return ingredient


def test_init_creates_empty_burger(burger):
    assert burger.bun is None
    assert burger.ingredients == []


def test_set_buns_sets_bun(burger, bun):
    burger.set_buns(bun)

    assert burger.bun is bun


def test_add_ingredient_adds_ingredient(burger, ingredient):
    burger.add_ingredient(ingredient)

    assert burger.ingredients == [ingredient]


def test_remove_ingredient_removes_by_index(burger):
    first = Mock()
    second = Mock()
    burger.ingredients = [first, second]

    burger.remove_ingredient(0)

    assert burger.ingredients == [second]


def test_move_ingredient_changes_order(burger):
    first = Mock()
    second = Mock()
    third = Mock()
    burger.ingredients = [first, second, third]

    burger.move_ingredient(0, 2)

    assert burger.ingredients == [second, third, first]



@pytest.mark.parametrize(
    "bun_price, ingredient_prices, expected_price",
    [
        (100, [], 200),
        (100, [50], 250),
        (80, [30, 20], 210),
    ],
)
def test_get_price_returns_correct_price(
    burger, bun, bun_price, ingredient_prices, expected_price):
    bun.get_price.return_value = bun_price
    burger.set_buns(bun)

    for price in ingredient_prices:
        ingredient = Mock()
        ingredient.get_price.return_value = price
        burger.add_ingredient(ingredient)

    assert burger.get_price() == expected_price



def test_get_receipt_returns_formatted_receipt(burger, bun, ingredient):
    burger.set_buns(bun)
    burger.add_ingredient(ingredient)

    expected_receipt = (
        "(==== black bun ====)\n"
        "= sauce hot sauce =\n"
        "(==== black bun ====)\n"
        "\n"
        "Price: 250"
    )

    assert burger.get_receipt() == expected_receipt
