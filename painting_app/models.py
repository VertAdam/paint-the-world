# # from django.contrib.gis.db import models
# from django.db import models
# # from django.contrib.gis.geos import Polygon
# from shapely.geometry import Polygon
# from .mapping import gridcoords_to_polygon, latlong_to_gridcoords
# import datetime
# # Create your models here.
#
# class UserData(models.Model):
#     userID = models.CharField(default = 9999999999, max_length = 100)
#     username = models.CharField(max_length = 100)
#     firstname = models.CharField(max_length=100)
#     lastname = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     sex = models.CharField(max_length=100)
#
#     class Meta:
#         verbose_name_plural = 'User Data'
#
#     def __str__ (self):
#         return self.username
#
# class AllGridData(models.Model):
#     # All Grids Ever Visited by anyone
#     activity_id = models.CharField(max_length=100)
#     userID = models.CharField(default=99999999, max_length=100)
#     latitude = models.FloatField(default=43.4495)
#     longitude = models.FloatField(default = -80.4285)
#     time = models.DateTimeField(default = datetime.datetime(1980,1,1))
#     grid_lat = models.PositiveIntegerField(default = 0)
#     grid_long = models.PositiveIntegerField(default = 0)
#
#     class Meta:
#         verbose_name_plural = 'All Grid Data'
#
#     # def save(self, *args, **kwargs):
#     #     self.grid_lat, self.grid_long = latlong_to_gridcoords(self.latitude, self.longitude)
#     #     return super().save(*args, **kwargs)
#
#
#     def __str__(self):
#         return self.activity_id
#
# class CanvasGridData(models.Model):
#     # All Grids Ever Visited by anyone
#     activity_id = models.CharField(max_length=100)
#     userID = models.CharField(default=99999999, max_length=100)
#     latitude = models.FloatField(default=43.4495)
#     longitude = models.FloatField(default = -80.4285)
#     time = models.DateTimeField(default = datetime.datetime(1980,1,1))
#     grid_lat = models.PositiveIntegerField(default = 0)
#     grid_long = models.PositiveIntegerField(default = 0)
#
#     # default_poly = ((-80.4285, 43.449499999999986), (-80.4275, 43.449499999999986), (-80.4275, 43.45049999999999),
#     #                 (-80.4285, 43.45049999999999),  (-80.4285, 43.449499999999986))
#     # polygon = models.PolygonField(default = Polygon(default_poly).wkt)
#
#     class Meta:
#         verbose_name_plural = 'Canvas Grid Data'
#
#     # def save(self, *args, **kwargs):
#     #     self.grid_lat, self.grid_long = latlong_to_gridcoords(self.latitude, self.longitude)
#         # self.polygon = gridcoords_to_polygon(self.grid_lat, self.grid_long).wkt
#         # return super().save(*args, **kwargs)
#
#
#     def __str__(self):
#         return self.activity_id