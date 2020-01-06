import sys
import logging

LOG = logging.getLogger(__name__)

def get_fname(stack_frame):
    fname = sys._getframe(stack_frame).f_code.co_name
    return fname

def log_message(msg):
    LOG.info('%s(): %s', get_fname(2), msg)

def log_entry():
    LOG.info('%s(): caller: %s: processing started...', get_fname(2), get_fname(3))    