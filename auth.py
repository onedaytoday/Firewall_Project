API_KEY = ""
import json
import meraki
import Layer3Firewall
class MerakiDash:
    def __init__(self, key = API_KEY):
        self.session = meraki.DashboardAPI(api_key=key)

    def get_firewall(self):
        Layer3Rules = self.session.appliance.getNetworkApplianceFirewallL3FirewallRules()
        ParsedRule = json.load(Layer3Rules)


        FireWallRules = []
        for rule in ParsedRule.rules:
            MerakiDash.__parse_firewall_rule(rule, FireWallRules)

    @staticmethod
    def __parse_firewall_rule(rule, parsedRule):
        Layer3Firewall.Layer3Firewall.FirewallRule()