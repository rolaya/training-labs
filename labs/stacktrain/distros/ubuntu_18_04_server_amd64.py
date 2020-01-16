#!/usr/bin/env python

# Force Python 2 to use float division even for ints
from __future__ import division
from __future__ import print_function

import logging
import os
import re
import sys

import stacktrain.core.cond_sleep as cs
import stacktrain.core.download as dl
import stacktrain.core.keycodes as kc
import stacktrain.config.general as conf
import stacktrain.distros.distro as distro
import stacktrain.core.log_utils as log_utils
import stacktrain.core.app_utils as app_utils

logger = logging.getLogger(__name__)

conf.base_install_scripts = "scripts.ubuntu_base"
conf.distro = "ubuntu"

# -----------------------------------------------------------------------------
# Installation from ISO image
# -----------------------------------------------------------------------------

class ISOImage(distro.GenericISOImage):
    logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
    def __init__(self, arch="amd64"):
        logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
        super(ISOImage, self).__init__()
        self.arch = arch
        if arch == "amd64":
            self.release_name = "ubuntu-18.04-amd64"
            self.url = ("http://cdimage.ubuntu.com/releases/18.04/release/"
                        "ubuntu-18.04.3-server-amd64.iso")
            self.md5 = "cb7cd5a0c94899a04a536441c8b6d2bf"
            # ostype used by VirtualBox to choose icon and flags (64-bit,
            # IOAPIC)
            conf.vbox_ostype = "Ubuntu_64"
        elif arch == "i386":
            logger.error("Arch: i386 unsupported in bionic. Aborting.")
            app_utils.exit(1)
        else:
            logger.error("Unknown arch: %s. Aborting.", arch)
            app_utils.exit(1)


    # Fallback function to find current ISO image in case the file in ISO_URL
    # is neither on the disk nor at the configured URL. This mechanism was
    # added because old Ubuntu ISOs are removed from the server as soon as a
    # new ISO appears.

    def update_iso_image_variables(self):
        logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))

        # Get matching line from distro repo's MD5SUMS file, e.g.
        # "9e5fecc94b3925bededed0fdca1bd417 *ubuntu-14.04.3-server-amd64.iso"
        md5_url = os.path.join(self.url_base, "MD5SUMS")
        logger.debug("About to download MD5SUM from %s", md5_url)
        try:
            txt = dl.downloader.download(md5_url)
        except EnvironmentError:
            logger.error("Can't find newer ISO image. Aborting.")
            app_utils.exit(1)

        if self.arch == "amd64":
            ma = re.search(r"(.*) \*{0,1}(.*server-amd64.iso)", txt)
        if ma:
            self.md5 = ma.group(1)
            self.name = ma.group(2)
            logger.info("Using new ISO image:\n\t%s\n\t%s", self.name,
                        self.md5)
        else:
            logger.error("Failed to update ISO location. Exiting.")
            app_utils.exit(1)

        logger.info("New ISO URL:\n\t%s", self.url)

PRESEED_HOST_DIR = ("https://opendev.org/openstack/training-labs/raw/branch/"
                     "master/labs/osbash/lib/osbash/netboot/")

PRESEED_URL = {}
PRESEED_URL['ssh'] = PRESEED_HOST_DIR + "preseed-ssh-v6.cfg"
PRESEED_URL['shared_folder'] = PRESEED_HOST_DIR + "preseed-vbadd-v7.cfg"
PRESEED_URL['all'] = PRESEED_HOST_DIR + "preseed-all-v7.cfg"

# Arguments for ISO image installer
_BOOT_ARGS = ("/install/vmlinuz"
              " noapic"
              " debian-installer/allow_unauthenticated_ssl=true"
              " preseed/url=%s"
              " debian-installer=en_US"
              " auto=true"
              " locale=en_US"
              " hostname=osbash"
              " fb=false"
              " debconf/frontend=noninteractive"
              " keyboard-configuration/modelcode=SKIP"
              " initrd=/install/initrd.gz"
              " console-setup/ask_detect=false")



def distro_start_installer(config):
    logger.info('%s(): caller: %s()', log_utils.get_fname(1), log_utils.get_fname(2))
    """Boot the ISO image operating system installer"""

    preseed = PRESEED_URL[conf.vm_access]

    logger.info('%s(): conf.vm_access: [%s]', log_utils.get_fname(1), conf.vm_access)

    logger.debug("Using %s", preseed)

    boot_args = _BOOT_ARGS % preseed

    if conf.vm_proxy:
        boot_args += " mirror/http/proxy=%s http_proxy=%s" % (conf.vm_proxy,
                                                              conf.vm_proxy)

    logger.debug("Choosing installer expert mode.")
    kc.keyboard_send_enter(config.vm_name)
    kc.keyboard_send_f6(config.vm_name)
    kc.keyboard_send_escape(config.vm_name)

    logger.debug("Clearing default boot arguments.")
    for _ in range(83):
        kc.keyboard_send_backspace(config.vm_name)

    logger.debug("Pushing boot command line: %s" , boot_args)
    kc.keyboard_send_string(config.vm_name, boot_args)

    logger.info("Initiating boot sequence for %s.", config.vm_name)
    kc.keyboard_send_enter(config.vm_name)
