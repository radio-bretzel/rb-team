TESTING = True
WTF_CSRF_ENABLED =  False

OBJECTS_NAME_PREFIX = 'radiobretzel_tests_'

MONGO_HOST = 'database.tests_main.radiobretzel'
MONGO_DBNAME = 'radiobretzel_test'

SOURCE_CONTAINER_IMAGE = 'radiobretzel/source:dev'

SOURCE_NETWORK = 'tests_sources'

STREAM_HOST = 'streaming.tests_sources.radiobretzel'
STREAM_SOURCE_PASSWD = 'sourcepasstest'
