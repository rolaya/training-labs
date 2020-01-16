import sys
import logging
import log_utils

LOG = logging.getLogger(__name__)

# Use this function for debugging purposes 
def exit(code):

    # Log name of function which invoked application termination
    fname = sys._getframe(1).f_code.co_name
    LOG.info('%s(): terminating application, exit code: [%s]', fname, code)
    sys.exit(code)
