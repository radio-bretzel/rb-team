# -*- coding: utf-8 -*-
"""
    rbteam.cli
    ~~~~~~~~~~

    Little command line interface for running the app.

    More info in documentation at https://docs.radiobretzel.org
"""


from argparse import ArgumentParser

from rbteam import create_app

PARSER = ArgumentParser()

PARSER.add_argument(
    '--debug',
    help="Run rb-team in debug mode. This argument is implicit when rb-team \
    is run in development or test environments.",
    dest="debug",
    action="store_true"
)

PARSER.add_argument(
    '-e', '--env', '--environment',
    help="Environment in which the app will run.",
    dest="environment",
    action="store",
    choices=['development', 'test', 'production'],
    default="production"
)

PARSER.add_argument(
    '--directory', '--instance-path',
    help="Instance directory. All relatives pathes given through cli argument, \
    configuration file or environment variables will be calculated from \
    this directory.",
    dest="instance_path",
    action="store"
)

PARSER.add_argument(
    '-f', '--config-file',
    help="Name of the configuration file. Can be absolute or relative path. \
    If relative path is given, it will be relative to the application instance \
    path (see --directory option)",
    dest="config_file",
    action="store"
)

# PARSER.add_argument(
#     '-l', '--log-file',
#     help="Path of the log file or directory.",
#     dest="LOG_FILE",
#     action="store",
#     default="radiobretzel-core.log"
# )


def main():
    """Alias for flask.run command
    """
    args = PARSER.parse_args()
    radiobretzel_core = create_app(**vars(args))

    radiobretzel_core.run(debug=True, use_reloader=False, host='0.0.0.0')
