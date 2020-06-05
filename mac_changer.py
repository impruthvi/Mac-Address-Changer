#!/usr/bin/env python

import subprocess
import optparse
import re


def get_arguments():
    parse = optparse.OptionParser()
    parse.add_option("-i", "--interface", dest="interface", help="interface to change mac address")
    parse.add_option("-m", "--mac", dest="mac_address", help="change mac address")
    (options, arguments) = parse.parse_args()
    if not options.interface:
        parse.error('pleas specify the interface,use --help for more info')
    elif not options.mac_address:
        parse.error('pleas specify the mac_address,use --help for more info')
    return options


def change_mac(interface, mac_address):
    print("change mac address for " + interface + " to " + mac_address)
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_address])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    # print(ifconfig_result)

    mac_address_search_address = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result)
    if mac_address_search_address:
        return mac_address_search_address.group(0)
    else:
        print("could not read mac address")


options = get_arguments()

current_mac = get_current_mac(options.interface)
print("current mac = " + str(current_mac))

change_mac(interface=options.interface, mac_address=options.mac_address)
current_mac = get_current_mac(options.interface)
if current_mac == options.mac_address:
    print("mac address change successfully changed to " + current_mac)
else:
    print("mac address not change")
