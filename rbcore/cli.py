from argparse import ArgumentParser
from os import path
from . import create_app

parser = ArgumentParser()

parser.add_argument('--debug',
    help="Run rb-core in debug mode. This argument is implicit when rb-core is run in development or test environments.",
    dest="debug",
    action="store_true")

parser.add_argument('-e', '--env', '--environment',
    help="Environment in which the app will run.",
    dest="environment",
    action="store",
    choices=['development', 'test', 'production'],
    default="production")

parser.add_argument('--directory', '--instance-path',
    help="Instance directory. All relatives pathes given through cli argument, configuration file or environment variables will be calculated from this directory.",
    dest="instance_path",
    action="store")

parser.add_argument('-f', '--config-file',
    help="Name of the configuration file. Can be absolute or relative path. If relative path is given, it will be relative to the application instance path (see --directory option)",
    dest="config_file",
    action="store")

# parser.add_argument('-l', '--log-file',
#     help="Path of the log file or directory.",
#     dest="LOG_FILE",
#     action="store",
#     default="radiobretzel-core.log")


def main():

    args = parser.parse_args()
    radiobretzel_core = create_app(**vars(args))

    radiobretzel_core.run(debug=True, use_reloader=False, host='0.0.0.0')
