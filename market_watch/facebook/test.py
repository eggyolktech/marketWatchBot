#!/usr/bin/python

from market_watch.util import logging_util

logging = logging_util.get_logger(__file__)

logging.debug('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')

