import pytest

import rb_backend

def test_database(app):
    with app.app_context():
        db_client = rb_backend.database.get_database()
        assert db_client.command('ping')

def test_database_error():
    config = {
        'MONGO_HOST': 'this defenitly not a good parameter',
        'MONGO_SERVER_SELECTION_TIMEOUT_MS': 5000
    }
    app = rb_backend.create_app('test', **config)
    assert app.config['MONGO_HOST'] == 'this defenitly not a good parameter'
    with app.app_context(), pytest.raises(rb_backend.errors.DatabaseError):
        db_client = rb_backend.database.get_database()
