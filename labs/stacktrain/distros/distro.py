#!/usr/bin/env python

# Force Python 2 to use float division even for ints
from __future__ import division
from __future__ import print_function

import os
import logging
import stacktrain.core.log_utils as log_utils

logger = logging.getLogger(__name__)

class GenericISOImage(object):
    logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))

    """Base class for ISO images"""

    def __init__(self):
        logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
        self.url_base = None
        self.name = None
        self.md5 = None

    @property
    def url(self):
        logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
        """"Return path to ISO image"""
        return os.path.join(self.url_base, self.name)

    @url.setter
    def url(self, url):
        logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
        """Update url_base and name based on new URL"""
        self.url_base = os.path.dirname(url)
        self.name = os.path.basename(url)
