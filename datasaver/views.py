from django.http import HttpResponse
from django.template import loader

def ttc(request):
    return HttpResponse(loader.get_template('ttc.html').render({
    }, request))
