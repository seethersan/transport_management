import json
from rest_framework import serializers
from .models import ServiceArea

from rest_framework import serializers
from django.contrib.gis.geos import Polygon
from .models import ServiceArea


class ServiceAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceArea
        fields = "__all__"

    def create(self, validated_data):
        geojson_data = validated_data.pop("geojson")
        # Convert the GeoJSON data to a Polygon object
        try:
            geojson_data = json.loads(geojson_data)
        except:
            pass
        polygon = Polygon(geojson_data["coordinates"][0])
        service_area = ServiceArea.objects.create(geojson=polygon, **validated_data)
        return service_area

    def update(self, instance, validated_data):
        geojson_data = validated_data.pop("geojson", None)
        if geojson_data:
            try:
                geojson_data = json.loads(geojson_data)
            except:
                pass
            # Convert the GeoJSON data to a Polygon object
            polygon = Polygon(geojson_data["coordinates"][0])
            instance.geojson = polygon

        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.provider = validated_data.get("provider", instance.provider)
        instance.save()
        return instance
