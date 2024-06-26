import pytest

from fast_zero.app import app


@pytest.fixture()
def client():
    return TestClient(app)
