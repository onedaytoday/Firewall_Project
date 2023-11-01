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


class InvalidSourceIP(DashExceptions):
    pass


class InvalidDestinationIP(DashExceptions):
    pass


class MissMatchedIPTypes(DashExceptions):
    pass
