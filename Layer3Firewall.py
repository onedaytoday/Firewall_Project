from enum import Enum


class Layer3Firewall:

    def __init__(self, rules):
        if len(rules) == 0:
            Exception()
        self.DEFAULT_DECISION = Layer3Firewall.Decision.NO_MATCH
        self.Rules = rules

    def print(self):
        for rule in self.Rules:
            rule.print()

    def filter(self, packet):
        for rule in self.Rules:
            decision = rule.rule_decision(packet)
            if decision == Layer3Firewall.Decision.Allow or decision == Layer3Firewall.Decision.Block:
                return decision
        return self.DEFAULT_DECISION

    def filter_multiple(self, packets):
        if len(packets) == 0:
            Exception()
        results = []
        for packet in packets:
            results.append(self.filter(packet))
        return results

    class Decision(Enum):
        NO_MATCH = 0
        Allow = 'Allow'
        Block = 'Block'

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

        def matches_rule(self, packet):
            src_port_match = self.src_port is None or self.src_port == 0 or self.src_port == packet.src_port
            dest_port_match = self.dest_port is None or self.dest_port == 0 or self.dest_port == packet.dest_port
            src_IP_match = self.src_ip_range is None or self.src_ip_range.ip_is_in_range(packet.src_ip)
            des_IP_match = self.dest_ip_range is None or self.dest_ip_range.ip_is_in_range(packet.dest_ip)

            return src_IP_match and des_IP_match and dest_port_match and src_port_match

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
                srcIP = self.src_ip_range.to_string()

            if self.dest_ip_range is None:
                desIP = "Any"
            else:
                desIP = self.dest_ip_range.to_string()

            print(f'{self.description} {self.action} {srcPort} {srcIP} {desIP} {desPort}')
