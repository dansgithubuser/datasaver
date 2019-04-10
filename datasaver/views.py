from django.http import JsonResponse
from django.shortcuts import render

import urllib.request

import math
import xml.etree.cElementTree

def ttc_vehicles_get(request):
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

def ttc_routes(request):
    response = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=routeList&a=ttc')
    tree = xml.etree.cElementTree.XML(response.read())
    routes = {i.attrib['tag']: i.attrib['title'] for i in tree.getchildren()}
    return render(request, 'ttc_routes.html', {'routes': routes})

def ttc_routes_get(request):
    tag = request.GET['tag']
    response = urllib.request.urlopen('http://webservices.nextbus.com/service/publicXMLFeed?command=routeConfig&a=ttc&r={}'.format(tag))
    tree = xml.etree.cElementTree.XML(response.read())
    route = tree.getchildren()[0]
    stops = [i for i in route.getchildren() if i.tag == 'stop']
    directions = [i for i in route.getchildren() if i.tag == 'direction']
    return JsonResponse({
        'latMin': route.attrib['latMin'],
        'latMax': route.attrib['latMax'],
        'lonMin': route.attrib['lonMin'],
        'lonMax': route.attrib['lonMax'],
        'stops': {i.attrib['tag']: {
            'title': i.attrib['title'],
            'lat': i.attrib['lat'],
            'lon': i.attrib['lon'],
        } for i in stops},
        'directions': {i.attrib['tag']: {
            'title': i.attrib['title'],
            'stops': [j.attrib['tag'] for j in i.getchildren()],
        } for i in directions},
    })
