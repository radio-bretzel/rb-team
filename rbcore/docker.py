import docker, time

from rbcore.config import get_config
from rbcore.errors import DockerError

def get_docker_client():
    """ Returns an instance of docker client
    """
    config = get_config()
    docker_config = config.get_namespace('DOCKER_')
    url = docker_config.pop('url')
    version = docker_config.pop('version')
    try:
        client = docker.DockerClient(
            base_url=url,
            version=version,
            **docker_config)
        return client
    except Exception as e:
        raise DockerError("Couldn't init docker connection : " + str(e))

def get_docker_network(name, **config):
    """This function returns a docker network depending on configuration given.
    Create the network if not found.
    """
    config = get_config()
    docker_client = get_docker_client()
    networks = docker_client.networks.list(name)
    if not networks:
        return docker_client.networks.create(name, **config)
    elif len(networks) > 1:
        raise DockerError('Matched multiple Docker networks named '+ name)
    else:
        network = networks[0]
    if not network:
        raise DockerError("Couldn't find nor create docker source network")
    return network
