import json

import meraki

import auth
import key

if __name__ == '__main__':
    session = meraki.DashboardAPI(key.API_KEY)
    print("Device:")
    device = session.devices.getDevice(key.MX_SERIAL)
    print(device)
    netID = device.get('networkId')
    L3Firewall = session.appliance.getNetworkApplianceFirewallL3FirewallRules(netID)
    print("Firewall L3 Rules")
    print(type(L3Firewall.get('rules')))
    print(L3Firewall)
    VLANs = session.appliance.getNetworkApplianceVlans(netID)

    #for V in VLANs:
        #print(V.get('ipv6').get('prefixAssignments')[0].get('staticPrefix'))

    print("VLANS")
    text = json.dumps(VLANs, sort_keys=True, indent=4)
    #print(text)
