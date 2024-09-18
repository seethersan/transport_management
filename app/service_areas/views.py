from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.core.cache import cache
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import ServiceArea
from .serializers import ServiceAreaSerializer


class ServiceAreaViewSet(viewsets.ModelViewSet):
    queryset = ServiceArea.objects.all()
    serializer_class = ServiceAreaSerializer


@swagger_auto_schema(
    method="get",
    operation_id="servicearea-latlng",
    manual_parameters=[
        openapi.Parameter(
            "lat", openapi.IN_QUERY, description="Latitude", type=openapi.TYPE_NUMBER
        ),
        openapi.Parameter(
            "lng", openapi.IN_QUERY, description="Longitude", type=openapi.TYPE_NUMBER
        ),
    ],
    responses={200: ServiceAreaSerializer(many=True)},
)
@api_view(["GET"])
def find_service_areas(request):
    lat = float(request.GET.get("lat"))
    lng = float(request.GET.get("lng"))
    cache_key = f"service_areas_{lat}_{lng}"

    data = cache.get(cache_key)
    if not data:
        point = Point(lng, lat, srid=4326)
        service_areas = ServiceArea.objects.filter(geojson__contains=point)
        data = ServiceAreaSerializer(service_areas, many=True).data
        cache.set(cache_key, data, timeout=60 * 15)  # Cache for 15 minutes

    return Response(data)
