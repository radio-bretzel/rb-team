SITE_NAME = 'Radio Bretzel backend'
OBJECTS_NAME_PREFIX = 'radiobretzel_'

API_AS_CONTAINER = True

DOCKER_URL = 'unix://var/run/docker.sock'
DOCKER_VERSION = 'auto'

MONGO_HOST = 'database.main.radiobretzel'
MONGO_DBNAME = 'radiobretzel'

SOURCE_TYPE = 'docker'
# DockerSource relative configuration
SOURCE_CONTAINER_IMAGE = 'radiobretzel/source:latest'
# SOURCE_CONTAINER_AUDIO_VOLUME = 'radiobretzel_audio'
SOURCE_NETWORK = True
SOURCE_NETWORK_NAME = 'sources'

STREAM_HOST = 'streaming.sources.radiobretzel'
STREAM_SOURCE_PASSWD = 'sourcepass'
