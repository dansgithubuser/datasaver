from django.urls import path
from . import views

urlpatterns=[
    path('ttc', views.ttc, name='ttc'),
]
