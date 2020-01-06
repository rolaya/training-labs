import logging
import stacktrain.config.general as conf
import stacktrain.core.autostart as autostart
import stacktrain.core.log_utils as log_utils
import stacktrain.batch_for_windows as wbatch

logger = logging.getLogger(__name__)

def build_nodes(cluster_cfg):
    logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
    config_name = "{}_{}".format(conf.distro, cluster_cfg)

    if conf.wbatch:
        wbatch.wbatch_begin_node(config_name)

    autostart.autostart_reset()
    autostart.autostart_from_config("scripts." + config_name)

    if conf.wbatch:
        wbatch.wbatch_end_file()
