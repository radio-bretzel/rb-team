#   Default configuration file.
#
#   This configuration will be merged with the corresponding environment
#   configuration. Any parameter described in one of the environment
#   configurations files will prevail on those described bellow. Following
#   content will be overriden if explicited through the different files in
#   this folder.
#
#   /!\
#             This file should not be edited by anyone except Radio
#             Bretzel development team. If you want to overide any of
#             these values please do it in local.py file.
#                                                                        /!\

class default(object):

   SITE_NAME = 'Radio Bretzel backend API'
   OBJECTS_NAME_PREFIX = 'radiobretzel_'

   DOCKER_URL = 'unix://var/run/docker.sock'
   DOCKER_VERSION = 'auto'

   MONGO_HOST = 'database.main.radiobretzel'
   MONGO_DBNAME = 'radiobretzel'

   SOURCE_IMAGE = 'radiobretzel/source:latest'
   # SOURCE_CONTAINER_AUDIO_VOLUME = 'radiobretzel_audio'
   SOURCE_NETWORK = 'sources'

   STREAM_HOST="streaming.sources.radiobretzel"
   STREAM_SOURCE_PASSWD="sourcepass"

class development(default):

   DEBUG = True
   ASSETS_DEBUG = True
   WTF_CSRF_ENABLED = False

   SOURCE_IMAGE = 'radiobretzel/source:dev'

class test(default):

   TESTING = True
   WTF_CSRF_ENABLED =  False
