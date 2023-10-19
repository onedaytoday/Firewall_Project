import json

import auth
import key
import meraki
def test_fire_wall_parsing():
    Dashboard = meraki.DashboardAPI(key.API_KEY)
    MXDevice = Dashboard.devices.getDevice(key.MX_SERIAL)
    print(MXDevice)
    print(type(MXDevice))
    networkId = MXDevice.get('networkId')
    print(MXDevice.get('networkId'))
    print(Dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(networkId))

    for rule in Dashboard.appliance.getNetworkApplianceFirewallL3FirewallRules(networkId).get('rules'):
        print(rule)


if __name__ == '__main__':
    test_fire_wall_parsing()
