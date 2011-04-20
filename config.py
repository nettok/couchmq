from ConfigParser import RawConfigParser


_config = RawConfigParser()
_config.read("couchmq.cfg")


server = _config.get('couchmq', 'server')
db = _config.get('couchmq', 'db')
