from django.contrib.gis.geos import Polygon
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from providers.models import Provider
from service_areas.models import ServiceArea


class ServiceAreaTests(APITestCase):
    def setUp(self):
        # Create a provider to associate with service areas
        self.provider = Provider.objects.create(
            name="Test Provider",
            email="testprovider@example.com",
            phone_number="123456789",
            language="EN",
            currency="USD",
        )

        # Create a polygon representing a service area
        self.polygon = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)))
        self.service_area_data = {
            "name": "Test Area",
            "price": 100.0,
            "provider": self.provider,
            "geojson": self.polygon,
        }
        self.service_area = ServiceArea.objects.create(**self.service_area_data)

    def test_create_service_area(self):
        url = reverse("servicearea-list")
        data = {
            "name": "New Area",
            "price": 150.0,
            "provider": self.provider.id,
            "geojson": {
                "type": "Polygon",
                "coordinates": [
                    [[0.0, 0.0], [0.0, 20.0], [20.0, 20.0], [20.0, 0.0], [0.0, 0.0]]
                ],
            },
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ServiceArea.objects.count(), 2)

    def test_retrieve_service_area(self):
        url = reverse("servicearea-detail", kwargs={"pk": self.service_area.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.service_area.name)

    def test_update_service_area(self):
        url = reverse("servicearea-detail", kwargs={"pk": self.service_area.id})
        updated_data = {
            "name": "Updated Area",
            "price": 200.0,
            "provider": self.provider.id,
            "geojson": {
                "type": "Polygon",
                "coordinates": [
                    [[0.0, 0.0], [0.0, 30.0], [30.0, 30.0], [30.0, 0.0], [0.0, 0.0]]
                ],
            },
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.service_area.refresh_from_db()
        self.assertEqual(self.service_area.name, "Updated Area")

    def test_delete_service_area(self):
        url = reverse("servicearea-detail", kwargs={"pk": self.service_area.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ServiceArea.objects.count(), 0)


class FindServiceAreasTests(APITestCase):
    def setUp(self):
        self.provider = Provider.objects.create(
            name="Test Provider",
            email="testprovider@example.com",
            phone_number="123456789",
            language="EN",
            currency="USD",
        )

        # Create two polygons representing service areas
        self.polygon_1 = Polygon(((0, 0), (0, 10), (10, 10), (10, 0), (0, 0)))
        self.polygon_2 = Polygon(((20, 20), (20, 30), (30, 30), (30, 20), (20, 20)))

        ServiceArea.objects.create(
            name="Area 1", price=100.0, provider=self.provider, geojson=self.polygon_1
        )
        ServiceArea.objects.create(
            name="Area 2", price=150.0, provider=self.provider, geojson=self.polygon_2
        )

    def test_find_service_areas_in_polygon(self):
        url = reverse("servicearea-latlng") + "?lat=5&lng=5"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "Area 1")

    def test_find_no_service_areas(self):
        url = reverse("servicearea-latlng") + "?lat=15&lng=15"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)
