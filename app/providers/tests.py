from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from providers.models import Provider


class ProviderTests(APITestCase):
    def setUp(self):
        # Create initial provider data
        self.provider_data = {
            "name": "Test Provider",
            "email": "testprovider@example.com",
            "phone_number": "123456789",
            "language": "EN",
            "currency": "USD",
        }
        self.provider = Provider.objects.create(**self.provider_data)

    def test_create_provider(self):
        url = reverse("provider-list")
        data = {
            "name": "New Provider",
            "email": "newprovider@example.com",
            "phone_number": "987654321",
            "language": "ES",
            "currency": "EUR",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Provider.objects.count(), 2)
        self.assertEqual(Provider.objects.get(id=2).name, "New Provider")

    def test_retrieve_provider(self):
        url = reverse("provider-detail", kwargs={"pk": self.provider.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], self.provider.name)

    def test_update_provider(self):
        url = reverse("provider-detail", kwargs={"pk": self.provider.id})
        updated_data = {
            "name": "Updated Provider",
            "email": "updatedprovider@example.com",
            "phone_number": "123456789",
            "language": "FR",
            "currency": "USD",
        }
        response = self.client.put(url, updated_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.provider.refresh_from_db()
        self.assertEqual(self.provider.name, "Updated Provider")

    def test_delete_provider(self):
        url = reverse("provider-detail", kwargs={"pk": self.provider.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Provider.objects.count(), 0)
