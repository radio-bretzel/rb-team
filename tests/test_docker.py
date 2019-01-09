import pytest

import rb_backend

def test_docker(app):
    with app.app_context():
        db_client = rb_backend.docker.get_docker_client()
        assert db_client.ping()

    app.config['DOCKER_URL'] = 'this defenitly not a good parameter'
    with app.app_context(), pytest.raises(rb_backend.errors.DockerError):
        db_client = rb_backend.docker.get_docker_client()
