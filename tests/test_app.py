import pytest

import rbteam

def test_default_routes(client):
    res = client.get('/')
    assert b'Welcome to Radio Bretzel' in res.data

def test_Sources_routes(client):
    assert client.get('/source').data == b'[]\n'

    assert client.get('/source/test-source-routes').status_code == 404
    assert client.post('/source/test-source-routes', data={'channel': 'dumb'}).status_code == 200
    assert client.get('/source/test-source-routes').status_code == 200
    assert client.put('/source/test-source-routes', data={'stream_mountpoint': 'new-mountpoint'}).status_code == 200
    assert client.get('/source/test-source-routes/start').status_code == 200
    assert client.get('/source/test-source-routes/stop').status_code == 200
    assert client.delete('/source/test-source-routes').status_code == 200

def test_Channels_controller(client):
    assert client.get('/channel/').data == b'[]\n'

    assert client.get('/channel/test-channel-routes').status_code == 404
    assert client.post('/channel/test_channel-routes').status_code == 400
    assert client.post('/channel/test-channel-routes').status_code == 200
    assert client.get('/channel/test-channel-routes').status_code == 200

    assert client.get('/channel/test-channel-routes/source').status_code == 200
    assert client.get('/channel/test-channel-routes/source/start').status_code == 200
    assert client.get('/channel/test-channel-routes/source/stop').status_code == 200

    assert client.delete('/channel/test-channel-routes', data={'hard_delete': 'true'}).status_code == 200
