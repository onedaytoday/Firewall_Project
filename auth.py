import logging
import time
import Layer3Firewall
import ipaddress

import json
import meraki
import Errors


class MerakiDash:
    def __init__(self, key):
        self.vlan_subnet_mapping = {}
        self.object_subnet_mapping = {}
        self.jsonRules = None
        self.orgID = None
        self.networkId = None
        try:
            self.session = meraki.DashboardAPI(api_key=key, output_log=False, suppress_logging=True)
        except:
            raise Errors.WrongDashKey()

    def fetch_network(self, serial):
        device = None
        self.MXSerial = serial
        try:
            device = self.session.devices.getDevice(serial)
        except:
            raise Errors.WrongSerial()
        try:
            self.networkId = device.get('networkId')
        except:
            raise Errors.NoNetworkFound()

        try:
            network = self.session.networks.getNetwork(self.networkId)
            self.orgID = network.get('organizationId')
        except:
            raise Errors.OrgIDProblem()

        if not 'MX' in device.get('model'):
            raise Errors.SerialNumberIsNotMX()
        try:
            self.resolveVLANIDtoIP()
        except:
            raise Errors.VLANProblems()

        try:
            self.resolveObjectstoIP()
        except:
            raise Errors.ObjectResolutionProblems()

    def get_network_info(self):
        networkInfo = self.session.networks.getNetwork(self.networkId)
        return networkInfo.get('name')

    @staticmethod
    def print_json_nicely(a):
        text = json.dumps(a, sort_keys=True, indent=4)
        # xprint("Device info: \n", text)

    def get_firewall(self):
        Layer3Rules = self.session.appliance.getNetworkApplianceFirewallL3FirewallRules(self.networkId)
        # MerakiDash.print_json_nicely(Layer3Rules)
        FireWallRules = []
        self.jsonRules = Layer3Rules.get('rules')
        for rule in Layer3Rules.get('rules'):
            try:
                createdRule = self.__parse_firewall_rule(rule)
                FireWallRules.append(createdRule)
            except:
                continue

        return Layer3Firewall.Layer3Firewall(FireWallRules)

    def resolveVLANIDtoIP(self):  # Method that handles turning a VLAN ID into CIDR
        try:
            self.VLANinfo = self.session.appliance.getNetworkApplianceVlans(self.networkId)
        except:
            raise Errors.VLANProblems()
        if self.VLANinfo == None or self.VLANinfo == []:
            return
        for vlan in self.VLANinfo:
            vlan_id = vlan['id']
            vlan_subnet = vlan['subnet']
            self.vlan_subnet_mapping[f"VLAN({vlan_id}).*"] = [ipaddress.ip_network(vlan_subnet)]
            if (vlan.get('ipv6') is not None and vlan.get('ipv6').get('prefixAssignments') is not None
                    and vlan.get('ipv6').get('prefixAssignments')[0] is not None and
                    vlan.get('ipv6').get('prefixAssignments')[0].get('staticPrefix') is not None):
                ipv6 = vlan.get('ipv6').get('prefixAssignments')[0].get('staticPrefix')
                if (ipv6 is not None):
                    self.vlan_subnet_mapping[f"VLAN({vlan_id}).*"].append(ipaddress.ip_network(ipv6))

    def get_vlan_id(self, ip_cidr):
        if ip_cidr in self.vlan_subnet_mapping:
            return self.vlan_subnet_mapping[ip_cidr]
        return ip_cidr

    def get_object_resolution(self, obj_id):
        if obj_id in self.object_subnet_mapping:
            return self.object_subnet_mapping[obj_id]

    def __parse_firewall_rule(self, rule):
        name = None
        description = None
        protocol = None
        src_port = None
        dest_port = None
        src_ip_range = []
        dest_ip_range = []
        policy = None

        policy = Layer3Firewall.Layer3Firewall.Decision.NO_MATCH
        if rule.get('policy') == 'allow':
            policy = Layer3Firewall.Layer3Firewall.Decision.Allow
        elif rule.get('policy') == 'deny':
            policy = Layer3Firewall.Layer3Firewall.Decision.Block

        # srcPort
        if rule.get('srcPort') == 'Any':
            src_port = None
        else:
            src_port = int(rule.get('srcPort'))

        # destPort
        if rule.get('destPort') == 'Any':
            dest_port = None
        else:
            dest_port = int(rule.get('destPort'))

        # srcIP
        if rule.get('srcCidr') == 'Any':
            src_ip_range = None
        else:
            for thisRule in rule.get('srcCidr').split(','):
                if 'VLAN' in thisRule:
                    temp = thisRule
                    src_ip_range.extend((self.get_vlan_id(temp)))
                elif 'OBJ' in thisRule:
                    temp = thisRule
                    src_ip_range.extend(self.get_object_resolution(temp))
                else:
                    src_ip_range.append(ipaddress.ip_network(thisRule))

        # destIP
        if rule.get('destCidr') == 'Any':
            dest_ip_range = None
        else:
            for thisRule in rule.get('destCidr').split(','):
                if 'VLAN' in thisRule:
                    temp = thisRule
                    dest_ip_range.extend((self.get_vlan_id(temp)))
                elif 'OBJ' in thisRule:
                    temp = thisRule
                    dest_ip_range.extend(self.get_object_resolution(temp))
                else:
                    dest_ip_range.append(ipaddress.ip_network(thisRule))

        output = Layer3Firewall.Layer3Firewall.FirewallRule(
            description=rule.get('comment'),
            decision=policy,
            src_ip_range=src_ip_range,
            dest_ip_range=dest_ip_range,
            srcport=src_port,
            destport=dest_port,
            protocol=rule.get('protocol')
        )

        return output

    def resolveObjectstoIP(self):
        objects = self.session.organizations.getOrganizationPolicyObjects(self.orgID)
        for object in objects:
            if object.get('category') == 'network' and object.get('type') == 'cidr':
                objectID = object.get('id')
                objectCIDR = object.get('cidr')
                self.object_subnet_mapping[f"OBJ({objectID})"] = [ipaddress.ip_network(objectCIDR)]


