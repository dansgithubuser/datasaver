from urllib.request import urlopen

from xml.etree.cElementTree import XML

url_nextbus = 'http://webservices.nextbus.com/service/publicXMLFeed?'
url_nextbus_vehicle_locations = url_nextbus + 'command=vehicleLocations&a=ttc&t=0'
url_nextbus_route_list = url_nextbus + 'command=routeList&a=ttc'
url_nextbus_route_config = url_nextbus + 'command=routeConfig&a=ttc&r={}'

class Error(Exception):
    def __init__(self, capture):
        Exception.__init__(self)
        self.capture = capture

def get_xml(url, capture_error=None):
    xml = XML(urlopen(url).read())
    if capture_error:
        capture = capture_error(xml)
        if capture: raise Error(capture)
    return xml

def get_xml_children(url, capture_error=None, filter=None):
    xml = get_xml(url, capture_error)
    return [i for i in xml.getchildren() if not filter or filter(i)]
