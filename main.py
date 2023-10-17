# TEAM IDEO Test Script
# Omid Najibzadeh
import meraki
import auth
import Layer3Firewall as Firewall
import Packet
import IPaddress
import server
version = "1.1"

def print_header():
    print(f'TEAM IDEO Project Version: {version}')
    print("------------------------------------------------")
    return


def print_footer():
    print("----------------------")
    print("END OF PROGRAM\n")

def test_firewall(firewall, packet):
    return firewall.filter(packet)

def test_and_print_firewall(firewall, packet):
    print()
    packet.print()
    print(test_firewall(firewall, packet))
    print()


def test():
    print_header()

    IPaddress_one = IPaddress.IPAddress(8,8,8,8)
    IPaddress_two = IPaddress.IPAddress(10,10,15,1)
    IPaddress_three = IPaddress.IPAddress(10,10,1,1)
    IPaddress_four = IPaddress.IPAddress(10,0,0,0)
    IPaddress_five = IPaddress.IPAddress(7,0,0,0)
    IPaddress_four.CIDR = 8


    FireWallRules = []
    FirewallRule1 = Firewall.Layer3Firewall.FirewallRule(Firewall.Layer3Firewall.Decision.Allow, None, IPaddress_one)
    FireWallRules.append(FirewallRule1)
    FirewallRule2 = Firewall.Layer3Firewall.FirewallRule(Firewall.Layer3Firewall.Decision.Allow, None, IPaddress_two)
    FireWallRules.append(FirewallRule2)
    FirewallRule3 = Firewall.Layer3Firewall.FirewallRule(Firewall.Layer3Firewall.Decision.Block, None, IPaddress_four)
    FireWallRules.append(FirewallRule3)


    print("Firewall Rules")
    print("\nPacket src_port src_ip des_ip des_port\n")

    MX_Firewall = Firewall.Layer3Firewall(FireWallRules)
    MX_Firewall.print()


    print("\nPacket Filtering and Decision\n")
    testPacket1 = Packet.Packet(None, IPaddress_one)
    test_and_print_firewall(MX_Firewall, testPacket1)

    testPacket2 = Packet.Packet(None, IPaddress_two)
    test_and_print_firewall(MX_Firewall, testPacket2)

    testPacket3 = Packet.Packet(None, IPaddress_three)
    test_and_print_firewall(MX_Firewall, testPacket3)

    testPacket4 = Packet.Packet(None, IPaddress_five)
    test_and_print_firewall(MX_Firewall, testPacket4)


    TestePackets = [testPacket1, testPacket2, testPacket3, testPacket4]
    print(MX_Firewall.filter_multiple(TestePackets))

    print_footer()



def test_IP_dot_to_IP_obj():
    result = IPaddress.IPAddress.make_ip_from_dot_notation_ip_string("10.0.0.1/31")
    result.print_dot_notation()


if __name__ == '__main__':
    server.result()


