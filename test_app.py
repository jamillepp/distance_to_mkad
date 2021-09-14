from app import create_app
import pytest


@pytest.fixture
def client():
    app = create_app()

    with app.test_client() as client:
        yield client


def test_string(client):

    rv = client.get('/getdistance/getaddress?address=Paris,+FR')
    assert rv.status_code == 200


def test_invalid(client):

    rv = client.get('/getdistance/getaddress?address=1125.054+14562.00')
    assert rv.status_code == 400


def test_insideMkad(client):

    rv = client.get('/getdistance/getaddress?address=55.785017+37.841576')
    assert rv.status_code == 400


def test_moscow(client):

    rv = client.get('/getdistance/getaddress?address=Moscow')
    assert rv.status_code == 200
