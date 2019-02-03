from django.http import HttpResponse, JsonResponse
from django.template import loader

import urllib.request

import json

def ttc(request):
    return HttpResponse(loader.get_template('ttc.html').render({
    }, request))

def ttc_vehicles(request):
    r = urllib.request.urlopen('http://restbus.info/api/agencies/ttc/vehicles')
    j = json.loads(r.read())
    return JsonResponse({'vehicles': j})
