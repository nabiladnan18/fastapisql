import pytest

from app.calculations import add, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    return BankAccount()


@pytest.fixture
def bank_account_50():
    return BankAccount(50)


@pytest.mark.parametrize(
    "num1, num2, expected", [(3, 2, 5), (4, 10, 14), (100, -1, 99)]
)
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected


def test_bank_set_initial_amount(bank_account_50):
    assert bank_account_50.balance == 50


def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0


def test_bank_withdraw(bank_account_50):
    bank_account_50.withdraw(20)
    assert bank_account_50.balance == 30


def test_bank_deposit(bank_account_50):
    bank_account_50.deposit(10)
    assert bank_account_50.balance == 60


def test_bank_collect_interest(bank_account_50):
    bank_account_50.collect_interest()
    assert round(bank_account_50.balance, 5) == 55


@pytest.mark.parametrize(
    "deposited, withdrew, expected",
    [(250, 50, 220), (100, 50, 55), (1200, 200, 1100)],
)
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    zero_bank_account.collect_interest()
    assert round(zero_bank_account.balance, 5) == expected


def test_insufficient_funds(bank_account_50):
    # the line below expects an exception to occur
    with pytest.raises(InsufficientFunds):
        bank_account_50.withdraw(200)
