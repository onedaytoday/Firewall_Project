import json
from enum import Enum
import ipaddress
import Errors


def is_in_range(a, b):

    if ((isinstance(a, ipaddress.IPv4Network) and isinstance(b, ipaddress.IPv4Address))
            or (isinstance(a, ipaddress.IPv6Network) or isinstance(b, ipaddress.IPv6Address))
    ):
        return b in a

    return False


class Layer3Firewall:

    def __init__(self, rules):
        if len(rules) == 0:
            Exception()
        self.DEFAULT_DECISION = Layer3Firewall.Decision.NO_MATCH
        self.Rules = rules

    def print(self):
        for rule in self.Rules:
            rule.print()


    def find_matching_rule(self, packet):
        for rule in self.Rules:
            decision = rule.rule_decision(packet)
            if decision == Layer3Firewall.Decision.Allow or decision == Layer3Firewall.Decision.Block:
                return decision, rule

        return self.DEFAULT_DECISION
    def filter(self, packet):
        for rule in self.Rules:
            decision = rule.rule_decision(packet)
            if decision == Layer3Firewall.Decision.Allow or decision == Layer3Firewall.Decision.Block:
                print()
                print("Rule that matched is")
                rule.print()
                print()
                return decision

        return self.DEFAULT_DECISION

    def filter_multiple(self, packets):
        if len(packets) == 0:
            Exception()
        results = []
        for packet in packets:
            results.append(self.filter(packet).value)
        return results

    def get_firewall_rules(self):
        output = []
        for rule in self.Rules:
            output.append(rule.get_rule_to_dic())
        return output

    class Decision(Enum):
        NO_MATCH = "no match"
        Allow = 'allow'
        Block = 'deny'

        def print(self):
            print(self.value)

        def get_value(self):
            return self.value

    class FirewallRule:

        def __init__(self, decision, src_ip_range, dest_ip_range, description="", protocol=None, srcport=0, destport=0):
            self.name = ""
            self.description = description
            self.protocol = protocol
            self.src_port = srcport
            self.dest_port = destport
            self.src_ip_range = src_ip_range
            self.dest_ip_range = dest_ip_range
            self.action = decision


        def get_rule_json(self):
            return json.dumps(self.get_rule_to_dic())
        def get_rule_to_dic(self):
            srcPort = ""
            desPort = ""
            srcIP = ""
            desIP = ""
            proto = ""
            if self.protocol is None:
                proto = "Any"
            if self.src_port is None or self.src_port == 0:
                srcPort = "Any"
            else:
                srcPort = str(self.src_port)
            if self.dest_port is None or self.dest_port == 0:
                desPort = "Any"
            else:
                desPort = str(self.dest_port)

            if self.src_ip_range is None:
                srcIP = "Any"
            else:
                srcIP = str(self.src_ip_range)

            if self.dest_ip_range is None:
                desIP = "Any"
            else:
                desIP = str(self.dest_ip_range)

            return {
                'comment': self.description,
                'policy': self.action.value,
                'protocol': proto,
                'srcPort': srcPort,
                'srcCidr': srcIP,
                'destPort': desPort,
                'destCidr': desIP,
                'syslogEnabled': False
            }

        def matches_rule(self, packet):
            src_port_match = self.src_port is None or self.src_port == 0 or self.src_port == packet.src_port
            dest_port_match = self.dest_port is None or self.dest_port == 0 or self.dest_port == packet.dest_port

            src_IP_match = False
            des_IP_match = False
            if self.src_ip_range is None:
                src_IP_match = True
            else:
                for ip_range in self.src_ip_range:
                    src_IP_match = (is_in_range(ip_range, packet.src_ip)
                                    or src_IP_match)
            if self.dest_ip_range is None:
                des_IP_match = True
            else:
                for ip_range in self.dest_ip_range:
                    des_IP_match = (is_in_range(ip_range, packet.dest_ip)
                                    or des_IP_match)
            proto_match = self.protocol is None or self.protocol == packet.protocol

            return src_IP_match and des_IP_match and dest_port_match and src_port_match and proto_match

        def rule_decision(self, packet):
            if self.matches_rule(packet):
                return self.action
            return Layer3Firewall.Decision.NO_MATCH

        def print(self):
            srcPort = ""
            desPort = ""
            srcIP = ""
            desIP = ""
            proto = ""
            if self.protocol is None:
                proto = "Any"
            if self.src_port is None or self.src_port == 0:
                srcPort = "Any"
            else:
                srcPort = str(self.src_port)

            if self.dest_port is None or self.dest_port == 0:
                desPort = "Any"
            else:
                desPort = str(self.dest_port)

            if self.src_ip_range is None:
                srcIP = "Any"
            else:
                srcIP = str(self.src_ip_range)

            if self.dest_ip_range is None:
                desIP = "Any"
            else:
                desIP = str(self.dest_ip_range)

            print(f'{self.description} {srcPort} {srcIP} {desIP} {desPort} {self.action}')
