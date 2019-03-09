from django.http import HttpResponse, JsonResponse
from django.template import loader

import urllib.request

import math
import xml.etree.cElementTree

def ttc(request):
    return HttpResponse(loader.get_template('ttc.html').render({
    }, request))

def ttc_vehicles(request):
    request_lat = float(request.GET['lat'])
    request_lon = float(request.GET['lon'])
    response = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=vehicleLocations&a=ttc&t=0')
    tree = xml.etree.cElementTree.XML(response.read())
    result = {}
    for i in tree.getchildren():
        if i.tag != 'vehicle': continue
        vehicle = i.attrib
        vehicle_lat = float(vehicle['lat'])
        vehicle_lon = float(vehicle['lon'])
        if abs(vehicle_lat - request_lat) + abs(vehicle_lon - request_lon) > 5e-2: continue
        speed=vehicle.get('speedKmHr')
        if speed is not None: speed=float(speed)
        result[vehicle['id']] = dict(
            route=vehicle['routeTag'],
            direction=vehicle['dirTag'],
            lat=vehicle_lat,
            lon=vehicle_lon,
            reportAge=float(vehicle['secsSinceReport']),
            predictable=vehicle['predictable'],
            heading=float(vehicle['heading']),
            speed=speed,
        )
    return JsonResponse(result)
