import IPaddress


class Packet:
    def __init__(self, source_ip, destination_ip, protocol=None, srcport=0, destport=0):
        self.protocol = protocol
        self.src_ip = source_ip
        self.dest_ip = destination_ip
        self.src_port = srcport
        self.dest_port = destport

    def print(self):
        protocol = ""
        srcPort = ""
        desPort = ""
        srcIP = ""
        if self.protocol == None:
            protocol = "Any"
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

        print(f'{srcPort} {srcIP} {desIP} {desPort}')
        return
