

class PortalTypeError(Exception):
    def __init__(self, message):
        self.message = message

class PortalNotWorking(Exception):
    def __init__(self, message):
        self.message = message
