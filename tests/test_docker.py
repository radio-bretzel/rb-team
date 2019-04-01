import pytest

import rbteam

def test_docker(app):
    with app.app_context():
        db_client = rbteam.docker.get_docker_client()
        assert db_client.ping()

    app.config['DOCKER_URL'] = 'this defenitly not a good parameter'
    with app.app_context(), pytest.raises(rbteam.errors.DockerError):
        db_client = rbteam.docker.get_docker_client()
