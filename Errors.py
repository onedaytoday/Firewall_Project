class DashExceptions(Exception):
    pass


class WrongDashKey(DashExceptions):
    pass


class WrongSerial(DashExceptions):
    pass


class NoNetworkFound(DashExceptions):
    pass


class VLANProblems(DashExceptions):
    pass

class InvalidSourceIP(Exception):
    pass


class InvalidDestinationIP(Exception):
    pass


class MissMatchedIPTypes(Exception):
    pass