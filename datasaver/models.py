from django.db import models

class Lock(models.Model):
    resource = models.TextField(db_index=True)
    locked = models.BooleanField()

class TtcRoute(models.Model):
    tag = models.TextField()
    title = models.TextField()
    lat_min = models.FloatField()
    lon_min = models.FloatField()
    lat_max = models.FloatField()
    lon_max = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)

class TtcStop(models.Model):
    tag = models.TextField()
    route = models.ForeignKey(TtcRoute, models.CASCADE, db_index=True)
    title = models.TextField()
    lat = models.FloatField()
    lon = models.FloatField()
    updated_at = models.DateTimeField(auto_now=True)
