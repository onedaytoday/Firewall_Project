import IPaddress
import key

API_KEY = key.API_KEY

import json
import meraki
import Layer3Firewall


class MerakiDash:
    def __init__(self, key, serial):
        self.session = meraki.DashboardAPI(api_key=key)
        self.MXSerial = serial
        self.networkId = self.session.devices.getDevice(serial).get('networkId')

    def get_firewall(self):
        Layer3Rules = self.session.appliance.getNetworkApplianceFirewallL3FirewallRules(self.networkId)

        FireWallRules = []
        for rule in Layer3Rules.get('rules'):
            FireWallRules.append(MerakiDash.__parse_firewall_rule(rule))
        return Layer3Firewall.Layer3Firewall(FireWallRules)

    @staticmethod
    def __parse_firewall_rule(rule):
        name = None
        description = None
        protocol = None
        src_port = None
        dest_port = None
        src_ip_range = None
        dest_ip_range = None
        policy = None

        policy = Layer3Firewall.Layer3Firewall.Decision.NO_MATCH
        if rule.get('policy') == 'allow':
            policy = Layer3Firewall.Layer3Firewall.Decision.Allow
        elif rule.get('policy') == 'deny':
            policy = Layer3Firewall.Layer3Firewall.Decision.Block

        #srcPort
        if rule.get('srcPort') == 'Any':
            src_port = 0
        else:
            src_port = int(rule.get('srcPort'))

        #destPort
        if rule.get('destPort') == 'Any':
            dest_port = 0
        else:
            dest_port = int(rule.get('destPort'))

        #srcIP
        if rule.get('srcCidr') == 'Any':
            src_ip_range = None
        elif 'VLAN' in rule.get('srcCidr'):
            print('Vlan')
        else:
            src_ip_range = IPaddress.IPAddress.make_ip_from_dot_notation_ip_string(rule.get('srcCidr'))

        #destIP
        if rule.get('destCidr') == 'Any':
            dest_ip_range = None
        elif 'VLAN' in rule.get('destCidr'):
            print('Vlan')
        else:
            dest_ip_range = IPaddress.IPAddress.make_ip_from_dot_notation_ip_string(rule.get('destCidr'))

        output = Layer3Firewall.Layer3Firewall.FirewallRule(
            description=rule.get('comment'),
            decision=policy,
            src_ip_range= src_ip_range,
            dest_ip_range=dest_ip_range,
            srcport=src_port,
            destport=dest_port
        )

        return output
    def get_vlan_IP(self, s):

        return

