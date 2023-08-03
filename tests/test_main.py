import pytest
from main import calculate_deposit, app
import datetime as dt


def test_valid_deposit():
    data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }
    data['date'] = dt.datetime.strptime(data['date'], "%d.%m.%Y").date()
    expected_result = {
        "31.01.2021": 10050,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75
    }
    result, status_code = calculate_deposit(data['date'], data['periods'], data['amount'], data['rate'])
    assert status_code == 200
    assert result == expected_result


def test_invalid_periods():
    data = {
        "date": "31.01.2021",
        "periods": 0,
        "amount": 10000,
        "rate": 6
    }
    data['date'] = dt.datetime.strptime(data['date'], "%d.%m.%Y").date()
    expected_error = {"error": "periods are not valid"}
    result, status_code = calculate_deposit(data['date'], data['periods'], data['amount'], data['rate'])
    assert status_code == 400
    assert result == expected_error


def test_invalid_amount():
    data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 9000,
        "rate": 6
    }
    data['date'] = dt.datetime.strptime(data['date'], "%d.%m.%Y").date()
    expected_error = {"error": "amount is not valid"}
    result, status_code = calculate_deposit(data['date'], data['periods'], data['amount'], data['rate'])
    assert status_code == 400
    assert result == expected_error


def test_invalid_rate():
    data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 9
    }
    expected_error = {"error": "rate is not valid"}
    data['date'] = dt.datetime.strptime(data['date'], "%d.%m.%Y").date()
    result, status_code = calculate_deposit(data['date'], data['periods'], data['amount'], data['rate'])
    assert status_code == 400
    assert result == expected_error


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


def test_valid_request(client):
    data = {
        "date": "31.01.2021",
        "periods": 3,
        "amount": 10000,
        "rate": 6
    }
    response = client.post('/', json=data)
    assert response.status_code == 200
    assert response.get_json() == {
        "31.01.2021": 10050,
        "28.02.2021": 10100.25,
        "31.03.2021": 10150.75
    }


def test_invalid_request(client):
    data = {
        "date": "31/01/2021",
        "periods": 0,
        "amount": 9000,
        "rate": 9
    }
    response = client.post('/', json=data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "data is not valid"}


def test_invalid_period_value(client):
    data = {
        "date": "31.01.2021",
        "periods": 61,
        "amount": 10000,
        "rate": 6
    }
    response = client.post('/', json=data)
    assert response.status_code == 400
    assert response.get_json() == {"error": "periods are not valid"}

