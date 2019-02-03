from django.urls import path
from . import views

urlpatterns=[
    path('ttc', views.ttc),
    path('ttc/vehicles', views.ttc_vehicles),
]
