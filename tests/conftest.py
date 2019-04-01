import pytest

import rbteam


@pytest.fixture
def app():
    return rbteam.create_app('test')

@pytest.fixture
def client(app):
    return app.test_client()
