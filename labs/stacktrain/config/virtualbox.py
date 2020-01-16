import os
import logging

import stacktrain.config.general as conf
import stacktrain.core.log_utils as log_utils

logger = logging.getLogger(__name__)

conf.provider = "virtualbox"
conf.share_name = "osbash"
conf.share_dir = conf.top_dir
conf.vm_ui = "headless"


def get_base_disk_path():
    
    logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))

    base_disk_path = os.path.join(conf.img_dir, conf.get_base_disk_name() + ".vdi")

    logger.info('%s(): conf.img_dir:   [%s]', log_utils.get_fname(1), conf.img_dir)
    logger.info('%s(): base_disk_path: [%s]', log_utils.get_fname(1), base_disk_path)

    return base_disk_path
