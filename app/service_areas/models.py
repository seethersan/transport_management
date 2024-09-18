from django.contrib.gis.db import models
from providers.models import Provider


class ServiceArea(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(
        Provider, on_delete=models.CASCADE, related_name="service_areas"
    )
    geojson = models.PolygonField()

    def __str__(self):
        return f"{self.name} - {self.provider.name}"
