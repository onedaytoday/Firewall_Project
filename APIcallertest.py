# Layer 3 firewall test policy match for Meraki

import meraki
import time
import json
import ipaddress


class L3FWmatching:  # Class with API calls and L3 matching methods
    def __init__(self):
        self.APIkey = input("Please define an API key for your org: ")
        self.L3FWresponse = None
        self.networkID = None
        self.vlan_subnet_mapping = {}

    def getDevice(self):  # Method that gets device data and formats it
        dashboard = meraki.DashboardAPI(self.APIkey)
        time.sleep(.5)
        self.serial = input("Please enter the serial number for the device you would like to get info from: ")
        self.devResponse = dashboard.devices.getDevice(self.serial)
        time.sleep(.5)
        text = json.dumps(self.devResponse, sort_keys=True, indent=4)
        print("Device info: \n", text)

    def resolveVLANIDtoIP(self):  # Method that handles turning a VLAN ID into CIDR
        dashboard = meraki.DashboardAPI(self.APIkey)
        time.sleep(.5)
        self.VLANinfo = dashboard.appliance.getNetworkApplianceVlans(self.networkID)
        time.sleep(.5)
        text = json.dumps(self.VLANinfo, sort_keys=True, indent=4)
        print("VLAN info: \n", text)

        for vlan in self.VLANinfo:
            vlan_id = vlan['id']
            vlan_subnet = vlan['subnet']
            self.vlan_subnet_mapping[f"VLAN({vlan_id}).*"] = vlan_subnet

    def getL3firewallrules(self):  # Method that gets L3 firewall rules and prints them
        self.networkID = input("Please enter network ID to fetch L3 rules: ")
        dashboard = meraki.DashboardAPI(self.APIkey)
        time.sleep(.5)
        self.L3FWresponse = dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(self.networkID)
        time.sleep(.5)
        obj.resolveVLANIDtoIP()
        time.sleep(.5)
        text = json.dumps(self.L3FWresponse, sort_keys=True, indent=4)
        print("L3 FW rules: \n", text)

    def matchFirewallPolicy(self, source_ip, dest_ip):  # Method that handles policy matching and prints out the results
        if self.L3FWresponse is None:
            print("L3 firewall rules not fetched. Please call getL3firewallrules first.")
            return

        matching_rule = None

        for rule in self.L3FWresponse['rules']:
            if (
                    rule['comment'] == "Default rule" and
                    rule['srcCidr'] == "Any" and
                    rule['destCidr'] == "Any" and
                    rule['protocol'] == "any" and
                    rule['policy'] == "allow"
            ):
                matching_rule = rule
                break
            if (
                    (rule['srcCidr'] == "Any" or self.ip_in_rule(source_ip,
                                                                 self.resolve_vlan_cidr(rule['srcCidr']))) and
                    (rule['destCidr'] == "Any" or self.ip_in_rule(dest_ip, self.resolve_vlan_cidr(rule['destCidr'])))
            ):
                matching_rule = rule
                break

        if matching_rule:
            if matching_rule['policy'] == 'allow':
                print("Matching L3 Firewall Rule:")
                text = json.dumps(matching_rule, sort_keys=True, indent=4)
                print(text)
            else:
                print("Matching L3 Firewall Rule:")
                text = json.dumps(matching_rule, sort_keys=True, indent=4)
                print(text)
        else:
            print("No matching L3 firewall rule found.")

    def ip_in_rule(self, ip, rule_cidr):  # Checks if IP is in a policy using IP library
        try:
            ip_obj = ipaddress.ip_address(ip)
            rule_cidrs = [rule.strip() for rule in rule_cidr.split(",")]
            for rule in rule_cidrs:
                network_obj = ipaddress.ip_network(rule, strict=False)
                if ip_obj in network_obj:
                    return True
            return False
        except ValueError:
            return False

    def resolve_vlan_cidr(self, cidr_str):  # Resolves VLAN ID to cidr subnet
        if cidr_str in self.vlan_subnet_mapping:
            return self.vlan_subnet_mapping[cidr_str]
        return cidr_str

    def methodDecision(self):  # Method that takes user input to decide which method to call

        while True:
            self.choice = int(input("1. Device info\n"
                                    "2. L3 firewall rules\n"
                                    "3. Exit\n"
                                    "Please choose which what you would like to do: "))

            if self.choice == 1:
                obj.getDevice()
            elif self.choice == 2:
                obj.getL3firewallrules()
                break
            elif self.choice == 3:
                return
            else:
                print("Invalid option, please select a number 1-3")


if __name__ == '__main__':
    obj = L3FWmatching()
    obj.methodDecision()

    if obj.choice == 2:
        source_ip = input("Enter the source IP: ")
        dest_ip = input("Enter the destination IP: ")
        obj.matchFirewallPolicy(source_ip, dest_ip)
