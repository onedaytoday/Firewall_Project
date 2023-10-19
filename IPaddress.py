class IPAddress:
    def __init__(self, firstocted, secondocted, thirdocted, fourthocted, cidr=32):
        self.IPocteds = [0, 0, 0, 0]
        self.CIDR = cidr
        self.IPocteds[0] = firstocted
        self.IPocteds[1] = secondocted
        self.IPocteds[2] = thirdocted
        self.IPocteds[3] = fourthocted
        self.IP = self.converting_ints_to_32bit_addresss(firstocted, secondocted, thirdocted, fourthocted)

    @staticmethod
    def make_ip_from_dot_notation_ip_string(str):
        octed = []
        temp = ""
        for s in str:
            if s == '.' or s == '/':
                octed.append(int(temp))
                temp = ""
            elif '0' <= s <= '9':
                temp = temp + s
            else:
                Exception()
        octed.append(int(temp))

        output = None
        if len(octed) == 4:
            output = IPAddress(octed[0], octed[1], octed[2], octed[3])
        elif len(octed) == 5:
            output = IPAddress(octed[0], octed[1], octed[2], octed[3], cidr=octed[4])
        else:
            Exception()
        return output

    def add_four_int_by_bits(self, firstocted, secondocted, thirdocted, fourthocted):
        if firstocted < 0 or secondocted < 0 or thirdocted < 0 or fourthocted < 0:
            Exception()
        fourthocted = fourthocted << 0
        thirdocted = thirdocted << 8
        secondocted = secondocted << 16
        firstocted = firstocted << 24

        return firstocted | secondocted | thirdocted | fourthocted

    def signed_int_to_unsigned(self, num):
        if num > 1:
            return num
        return num & 0xffffffff

    def converting_ints_to_32bit_addresss(self, firstocted, secondocted, thirdocted, fourthocted):
        if firstocted < -1 or secondocted < -1 or thirdocted < -1 or fourthocted < -1:
            Exception()
        a = self.signed_int_to_unsigned(firstocted)
        b = self.signed_int_to_unsigned(secondocted)
        c = self.signed_int_to_unsigned(thirdocted)
        d = self.signed_int_to_unsigned(fourthocted)
        return self.add_four_int_by_bits(a, b, c, d)

    def calculate_network_address(self):
        return self.IP & 0xFFFFFFFF << (32 - self.CIDR)

    def calculate_network_address_with_cidr(self, cidr):
        return self.IP & 0xFFFFFFFF << (32 - cidr)

    def print(self):
        print(self.IP)

    def print_dot_notation(self):
        print(f"{self.IPocteds[0]}.{self.IPocteds[1]}.{self.IPocteds[2]}.{self.IPocteds[3]}/{self.CIDR}")

    def to_string(self):
        return (f"{self.IPocteds[0]}.{self.IPocteds[1]}.{self.IPocteds[2]}.{self.IPocteds[3]}/{self.CIDR}")

    def print_network_address(self):
        return print(self.calculate_network_address())

    def print_binary(self):
        print(bin(self.IP))

    def convert_int_to_ip(val):
        a = val & 0x000000FF
        val = val >> 8
        b = val & 0x000000FF
        val = val >> 8
        c = val & 0x000000FF
        val = val >> 8
        d = val & 0x000000FF
        return IPAddress(d, c, b, a)

    def is_range(self):
        return self.CIDR != 32

    def ip_is_in_range(self, ip):
        networkAddressRange = self.calculate_network_address()
        networkPortionOfIP = ip.calculate_network_address_with_cidr(self.CIDR)
        if networkPortionOfIP == networkAddressRange:
            return True
        return False
