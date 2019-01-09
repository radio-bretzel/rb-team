import pytest
import rb_backend

@pytest.fixture
def docker_source_app():
    config = {
        'SOURCE_TYPE': 'docker'
    }
    return rb_backend.create_app('test', **config)

def test_dockerSource_defaults(docker_source_app):
    with docker_source_app.app_context():
        test_source = rb_backend.source.source.init('test-source-docker')
        assert test_source.stream_mountpoint == 'test-source-docker'
        assert not test_source._get_container(quiet=True)
        test_source.create()
        assert test_source._get_container()
        with pytest.raises(rb_backend.errors.SourceError):
            test_source.create()
        assert test_source.create(force=True)
        assert test_source.status == 'stopped'
        test_source.start()
        assert test_source.status == 'playing'
        assert test_source.start(quiet=True)
        with pytest.raises(rb_backend.errors.SourceError):
            test_source.delete()
        test_source.stop()
        assert test_source.status == 'stopped'
        assert test_source.stop(quiet=True)
        test_source.delete()
        assert test_source.status == 'non-existent'
        assert test_source.delete(quiet=True)
        docker_source_app.config.update({'DOCKER_URL': 'nowhere'})
        assert test_source.status == 'in error'

def test_source_model(app):
    with app.app_context():
        test_source_models = rb_backend.source.model.Sources.find()
        assert test_source_models == []
        test_source_model = rb_backend.source.model.Sources.create(**{'name': 'test-source-model', 'channel': 'dumb'})
        assert test_source_model._document == {
            'name': 'test-source-model',
            'channel': 'dumb',
            'status': 'stopped',
            'stream_mountpoint': 'test-source-model'
        }
        test_source_model = rb_backend.source.model.Sources.find_one(**{'name': 'test-source-model'})
        with pytest.raises(rb_backend.errors.SourceError):
            test_source_model.create()
        test_source_model = rb_backend.source.model.Sources.update(test_source_model)
        assert test_source_model.status == 'stopped'
        test_source_model = rb_backend.source.model.Sources.update('test-source-model', **{'stream_mountpoint': 'ladida'})
        assert test_source_model.stream_mountpoint == 'ladida'
        test_source_model = rb_backend.source.model.Sources.delete(test_source_model)
        assert test_source_model.status == 'non-existent'
        with pytest.raises(rb_backend.errors.DatabaseNotFound):
            rb_backend.source.model.Sources.find_one(**{'name': 'test-source-model'})
