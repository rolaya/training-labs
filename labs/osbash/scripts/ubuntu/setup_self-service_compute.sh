#!/usr/bin/env bash

set -o errexit -o nounset

TOP_DIR=$(cd $(cat "../TOP_DIR" 2>/dev/null||echo $(dirname "$0"))/.. && pwd)

source "$TOP_DIR/config/paths"
source "$CONFIG_DIR/credentials"
source "$LIB_DIR/functions.guest.sh"
source "$CONFIG_DIR/openstack"

exec_logfile

indicate_current_auto

#------------------------------------------------------------------------------
# Networking Option 2: Self-service networks
# https://docs.openstack.org/neutron/stein/install/compute-install-option2-ubuntu.html
#------------------------------------------------------------------------------

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Configure the ML2 agent (one of Linux bridge, Open vSwitch)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# The configuration file is either "openvswitch_agent.ini" or "linuxbridge_agent.ini"
conf=/etc/neutron/plugins/ml2/$ML2_AGENT_CONF_FILE
echo "Configuring the $ML2_AGENT_DESC agent: [$ML2_AGENT], configuration file: [$conf]."

if [ "$ML2_AGENT" = "linuxbridge" ]; then

    # Edit the [linux_bridge] section.
    set_iface_list
    PUBLIC_INTERFACE_NAME=$(ifnum_to_ifname 2)
    echo "PUBLIC_INTERFACE_NAME=$PUBLIC_INTERFACE_NAME"
    iniset_sudo $conf linux_bridge physical_interface_mappings provider:$PUBLIC_INTERFACE_NAME

    # Edit the [vxlan] section.
    OVERLAY_INTERFACE_IP_ADDRESS=$(get_node_ip_in_network "$(hostname)" "mgmt")
    iniset_sudo $conf vxlan enable_vxlan true
    iniset_sudo $conf vxlan local_ip $OVERLAY_INTERFACE_IP_ADDRESS
    iniset_sudo $conf vxlan l2_population true

    # Edit the [securitygroup] section.
    iniset_sudo $conf securitygroup enable_security_group true
    iniset_sudo $conf securitygroup firewall_driver neutron.agent.linux.iptables_firewall.IptablesFirewallDriver

    echo "Ensuring that the kernel supports network bridge filters."
    if ! sudo sysctl net.bridge.bridge-nf-call-iptables; then
        sudo modprobe br_netfilter
        echo "# bridge support module added by training-labs" >> /etc/modules
        echo br_netfilter >> /etc/modules
    fi
else
    echo "Warning: $ML2_AGENT_DESC support pending."
fi

