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

class InvalidPort(DashExceptions):
    pass


class MissMatchedIPTypes(DashExceptions):
    pass

class SerialNumberIsNotMX(DashExceptions):
    pass

class InvalidFile(DashExceptions):
    pass

class VLANProblems(DashExceptions):
    pass


class OrgIDProblem(DashExceptions):
    pass


class ObjectResolutionProblems(DashExceptions):
    pass
