import ipaddress
import Errors
class Packet:
    def __init__(self, source_ip, destination_ip, protocol=None, srcport=None, destport=None):
        self.protocol = protocol
        self.src_ip = None
        self.set_src_IP(source_ip)
        self.dest_ip = None
        self.set_dest_IP(destination_ip)
        self.check_IP_types()
        self.src_port = None
        self.dest_port = None
        self.set_src_port(srcport)
        self.set_dest_port(destport)




    def set_src_IP(self, src):
        try:
            self.src_ip = ipaddress.ip_address(src)
        except:
            raise Errors.InvalidSourceIP()

    def set_dest_IP(self, dest):
        try:
            self.dest_ip = ipaddress.ip_address(dest)
        except:
            raise Errors.InvalidDestinationIP()


    def set_src_port(self, port):
        try:
            self.src_port = port
            if port is None or port is '':
                None
            elif not (0 < int(port) < 65536):
                raise Exception()
        except:
            raise Errors.InvalidPort()

    def set_dest_port(self, port):
        try:
            self.dest_port = port
            if port is None or port is '':
                None
            elif not (0 < int(port) < 65536):
                raise Exception()
        except:
            raise Errors.InvalidPort()
    def print(self):
        protocol = ""
        srcPort = ""
        desPort = ""
        srcIP = ""
        if self.protocol == None:
            protocol = "Any"
        else:
            protocol = self.protocol
        if self.src_port == None or self.src_port == 0:
            srcPort = "Any"
        else:
            srcPort = str(self.src_port)

        if self.dest_port == None or self.dest_port == 0:
            desPort = "Any"
        else:
            desPort = str(self.dest_port)

        if self.src_ip == None:
            srcIP = "Any"
        else:
            srcIP= str(self.src_ip)

        if self.dest_ip == None:
            desIP = "Any"
        else:
            desIP= str(self.dest_ip)

        print(f'{srcPort} {srcIP} {desIP} {desPort} {protocol}')
        return

    def to_string(self):
        protocol = ""
        srcPort = ""
        desPort = ""
        srcIP = ""
        if self.protocol == None:
            protocol = "Any"
        else:
            protocol = str(self.protocol)
        if self.src_port == None or self.src_port == 0:
            srcPort = "Any"
        else:
            srcPort = str(self.src_port)

        if self.dest_port == None or self.dest_port == 0:
            desPort = "Any"
        else:
            desPort = str(self.dest_port)

        if self.src_ip == None:
            srcIP = "Any"
        else:
            srcIP=self.src_ip.to_string()

        if self.dest_ip == None:
            desIP = "Any"
        else:
            desIP= self.dest_ip.to_string()

        space = " "
        return protocol + space + srcPort + space + srcIP + space + desIP + space + desPort

    def check_IP_types(self):
        if type(self.src_ip) != type(self.dest_ip):
            raise Errors.MissMatchedIPTypes()


