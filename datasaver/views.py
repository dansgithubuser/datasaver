from . import helpers

from django.http import JsonResponse
from django.shortcuts import render

import urllib.request

import math

def ttc_vehicles_get(request):
    request_lat = float(request.GET['lat'])
    request_lon = float(request.GET['lon'])
    try: vehicles = helpers.get_xml_children(
        helpers.url_nextbus_vehicle_locations,
        lambda xml: [i for i in xml if i.tag == 'Error'],
        lambda i: i.tag == 'vehicle',
    )
    except helpers.Error as e:
        error = [i.text.strip() for i in e.capture]
        if len(error) == 1: error = error[0]
        return JsonResponse({'error': error}, status=502)
    result = {}
    for i in vehicles:
        vehicle = i.attrib
        vehicle_lat = float(vehicle['lat'])
        vehicle_lon = float(vehicle['lon'])
        if abs(vehicle_lat - request_lat) + abs(vehicle_lon - request_lon) > 5e-2: continue
        speed=vehicle.get('speedKmHr')
        if speed is not None: speed=float(speed)
        result[vehicle['id']] = dict(
            route=vehicle['routeTag'],
            direction=vehicle.get('dirTag', '???'),
            lat=vehicle_lat,
            lon=vehicle_lon,
            reportAge=float(vehicle['secsSinceReport']),
            predictable=vehicle['predictable'],
            heading=float(vehicle['heading']),
            speed=speed,
        )
    return JsonResponse(result)

def ttc_routes(request):
    xml = helpers.get_xml_children(helpers.url_nextbus_route_list)
    routes = {i.attrib['tag']: i.attrib['title'] for i in xml}
    return render(request, 'ttc_routes.html', {'routes': routes})

def ttc_routes_get(request):
    tag = request.GET['tag']
    route = helpers.get_xml_children(helpers.url_nextbus_route_config.format(tag))[0]
    stops = [i for i in route if i.tag == 'stop']
    directions = [i for i in route if i.tag == 'direction']
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
            'stops': [j.attrib['tag'] for j in i],
        } for i in directions},
    })

def ttc_performance_get(request):
    helpers.ttc_routes_maintain()
    return JsonResponse({
    })
