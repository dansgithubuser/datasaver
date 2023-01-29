from . import models

from django.db import transaction

import defusedxml.ElementTree as ET

from urllib.request import urlopen

import collections
import datetime
import pytz
import types

url_nextbus = 'https://retro.umoiq.com/service/publicXMLFeed?'
url_nextbus_vehicle_locations = url_nextbus + 'command=vehicleLocations&a=ttc&t=0'
url_nextbus_route_list = url_nextbus + 'command=routeList&a=ttc'
url_nextbus_route_config = url_nextbus + 'command=routeConfig&a=ttc&r={}&terse'

class F:
    xml_last_raw: None

class Error(Exception):
    def __init__(self, capture):
        Exception.__init__(self)
        self.capture = capture

class Unlocker:
    def __init__(self, lock): self.lock = lock
    def __enter__(self): pass
    def __exit__(self, e_type, e_value, e_traceback): self.lock.update(locked=False)

class Bulker:
    def __init__(self, model, key):
        self.model = model
        self.key = key
        self.existing = {getattr(i, key): i for i in model.objects.all()}
        self.to_create = []

    def upsert(self, key, fields):
        self.fields = fields.keys()
        result = self.existing.get(key)
        if result:
            for k, v in fields.items(): setattr(result, k, v)
        else:
            result = self.model(**dict(fields, **{self.key: key}))
            self.to_create.append(result)
        return result

    def save(self):
        for l in [self.existing.values(), self.to_create]:
            for i in l:
                for f in self.fields:
                    field = getattr(i, f)
                    if type(field) == types.LambdaType:
                        setattr(i, f, field())
        self.model.objects.bulk_update(self.existing, self.fields)
        self.model.objects.bulk_create(self.to_create)

def now_utc(): return datetime.datetime.now(tz=pytz.utc)

def get_xml(url, capture_error=None):
    raw = urlopen(url).read()
    F.xml_last_raw = raw
    xml = ET.fromstring(raw)
    if capture_error:
        capture = capture_error(xml)
        if capture: raise Error(capture)
    return xml

def get_xml_children(url, capture_error=None, filter=None):
    xml = get_xml(url, capture_error)
    return [i for i in xml if not filter or filter(i)]

def ttc_routes_maintain():
    with transaction.atomic():
        lock = models.Lock.objects.filter(resource='ttc_routes').select_for_update()
        if lock[0].locked: return
        lock.update(locked=True)
    with Unlocker(lock) as unlocker:
        yesterday = now_utc() - datetime.timedelta(days=1)
        if models.TtcRoute.objects.filter(updated_at__gt=yesterday).count(): return
        #main
        routes = Bulker(models.TtcRoute, 'tag')
        stops = Bulker(models.TtcStop, 'tag')
        for route_entry in get_xml_children(url_nextbus_route_list):
            print('getting route {}'.format(route_entry.attrib['tag']))
            route_config = get_xml_children(
                url_nextbus_route_config.format(route_entry.attrib['tag'])
            )
            if len(route_config) != 1: raise Exception('route config has more than one child')
            route_config = route_config[0]
            route = routes.upsert(route_config.attrib['tag'], {
                'title': route_config.attrib['title'],
                'lat_min': route_config.attrib['latMin'],
                'lon_min': route_config.attrib['lonMin'],
                'lat_max': route_config.attrib['latMax'],
                'lon_max': route_config.attrib['lonMax'],
            })
            for i in route_config:
                if i.tag != 'stop': continue
                stop = stops.upsert(i.attrib['tag'], {
                    'route_id': lambda: route.id,
                    'title': i.attrib['title'],
                    'lat': float(i.attrib['lat']),
                    'lon': float(i.attrib['lon']),
                })
        routes.save()
        stops.save()
        #delete old
        yesterhour = now_utc() - datetime.timedelta(hours=1)
        models.TtcRoute.objects.filter(updated_at__lt=yesterhour).delete()
        models.TtcStop.objects.filter(updated_at__lt=yesterhour).delete()
