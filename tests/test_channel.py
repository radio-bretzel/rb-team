import pytest

import rbteam

def test_Channel(app):
    with app.app_context():
        test_channel = rbteam.channel.model.Channel(**{
            'slug': 'test-channel',
            'description': 'This is a nice description'
        })
        assert test_channel.name == 'Test Channel'
        assert test_channel.active == True
        assert test_channel.deleted == False
        assert test_channel.description == 'This is a nice description'

def test_Channels_model(app):
    with app.app_context():
        test_channel = rbteam.channel.model.Channels.create(**{'slug': 'test-channel-model'})
        assert test_channel.deleted == False
        test_channel = rbteam.channel.model.Channels.find_one(**{'slug': 'test-channel-model'})
        test_channel = rbteam.channel.model.Channels.update(test_channel, {'description': 'This is a nicer description'})
        assert test_channel.description == 'This is a nicer description'
        soft_deleted_channel = rbteam.channel.model.Channels.delete('test-channel-model')
        assert soft_deleted_channel.deleted == True
        with pytest.raises(rbteam.errors.DatabaseNotFound) as e:
            rbteam.channel.model.Channels.find_one(**{'slug': 'test-channel-model'})
        test_channel = rbteam.channel.model.Channels.find_one(**{'slug': 'test-channel-model', 'deleted': 'true'})
        rbteam.channel.model.Channels.delete(test_channel, hard_delete='true')
        with pytest.raises(rbteam.errors.DatabaseNotFound) as e:
            rbteam.channel.model.Channels.find_one(**{'slug': 'test-channel-model', 'deleted': 'true'})
