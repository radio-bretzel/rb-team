import pytest

import rbcore


@pytest.fixture
def app():
    return rbcore.create_app('test')

@pytest.fixture
def client(app):
    return app.test_client()
