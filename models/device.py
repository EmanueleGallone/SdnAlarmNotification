
class Device(object):
    def __init__(self, ip, netconf_rate, netconf_port, user, password):
        self.ip = ip
        self.netconf_rate = netconf_rate
        self.netconf_port = netconf_port
        self.user = user
        self.password = password
