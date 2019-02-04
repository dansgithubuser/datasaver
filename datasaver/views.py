from django.http import HttpResponse, JsonResponse
from django.template import loader

import urllib.request

import json

def ttc(request):
    return HttpResponse(loader.get_template('ttc.html').render({
    }, request))

def ttc_vehicles(request):
    lat = float(request.GET['lat'])
    lon = float(request.GET['lon'])
    r = urllib.request.urlopen('http://restbus.info/api/agencies/ttc/vehicles')
    j = json.loads(r.read())
    result = {}
    for i in j:
        if abs(i['lat'] - lat) + abs(i['lon'] - lon) > 5e-2: continue
        result[i['id']] = dict(
            lat=float(i['lat']),
            lon=float(i['lon']),
            heading=float(i['heading']),
            routeId=i['routeId'],
            directionId=i['directionId'],
            predictable=i['predictable'],
            leadingVehicleId=i['leadingVehicleId'],
            secsSinceReport=float(i['secsSinceReport']),
        )
    return JsonResponse(result)
