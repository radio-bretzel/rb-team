# -*- coding: utf-8 -*-
"""
    rbcore
    ~~~~~~

    Radio Bretzel core application. It allows you to manage channels, sources,
    chat rooms, and permissions for a team.
    This module follows the PEP8 programming convention and is documented on
    our website at https://www.radiobretzel.org

    More info in documentation at https://docs.radiobretzel.org
"""

__version__ = '0.2.1'

# rbcore module public interface
from rbcore.app import create_app
