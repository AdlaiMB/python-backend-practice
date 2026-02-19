import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.mark.parametrize("num1, num2, expected", [(3,3,6),(3,2,5),(12,12,24),(32, 12, 44)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(5, 3) == 2

def test_multiply():
    assert multiply(4, 3) == 12

def test_divide():
    assert divide(12, 2) == 6

def test_bank_set_initial_amount(bank_account):    
    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_bank_withdraw(bank_account):
    bank_account.withdraw(20)

    assert bank_account.balance == 30

def test_bank_deposit(bank_account):
    bank_account.deposit(90)

    assert bank_account.balance == 140

def test_bank_collect_interest(bank_account):
    bank_account.collect_interest()

    assert round(bank_account.balance, 6) == 55

@pytest.mark.parametrize("deposited, withdrew, expected", [(3,3,0),(100,50,50),(300,120,180),(90, 27, 63)])
def test_bank_transaction(zero_bank_account,  deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)

    assert zero_bank_account.balance == expected

def test_bank_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)

