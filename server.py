import configparser, falcon, json
from miio import airpurifier_miot

class AirPurifiersResource(object):
    devices = {}

    def __init__(self, devices):
        self.devices = devices

    def on_get(self, req, resp):
        status_by_device = { k: self.devices[k].status().data for k in self.devices }
        resp.body = json.dumps([ {'device': k, **status_by_device[k] } for k in status_by_device ])


config = configparser.ConfigParser()
config.read('config.ini')

# This is a horrible, horrible, horrible hack because ini files are sadness and
# I don't need to care too much for this. PRs welcome to change to a better
# format.
airpurifier_configs = filter(lambda k: k.startswith('airpurifier-'), config)

airpurifiers = { k: airpurifier_miot.AirPurifierMiot(ip=config[k]['ip'], token=config[k]['token']) for k in airpurifier_configs }

api = falcon.API()
airpurifiers_endpoint = AirPurifiersResource(airpurifiers)
api.add_route('/airpurifiers', airpurifiers_endpoint)
