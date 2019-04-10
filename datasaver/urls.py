from . import views

from django.urls import path
from django.views.generic import TemplateView

ttc_vehicles_view = TemplateView.as_view(template_name='ttc_vehicles.html')

urlpatterns = [
    path('ttc/vehicles', ttc_vehicles_view),
    path('ttc/vehicles/get', views.ttc_vehicles_get),
    path('ttc/routes', views.ttc_routes),
    path('ttc/routes/get', views.ttc_routes_get),
]
