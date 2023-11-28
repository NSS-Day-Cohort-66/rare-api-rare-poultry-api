import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import Categories

class CategoryTests(APITestCase):

    fixtures = ['categories', 'users', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_categories(self):
        url = "/categories"

        data = {
            "label": "Music"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["label"], "Music")
        self.assertEqual(json_response["id"], 3)

    def test_get_category(self):
        category = Categories()
        category.label = "Hobbies"
        category.save()

        response = self.client.get(f"/categories/{category.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Hobbies")
        self.assertEqual(json_response["id"], category.id)
        
    def test_get_categories(self):
        category = Categories()
        category.label = "Hobbies"
        category.save()

        response = self.client.get(f"/categories/{category.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Hobbies")
        self.assertEqual(json_response["id"], category.id)

    def test_change_tags(self):
        category = Categories()
        category.label = "Hobbies"
        category.save()

        data = {
            "label": "Wellness"
        }
        response = self.client.put(f"/categories/{category.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/categories/{category.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Wellness")

    # def test_delete_tag(self):
    #     category = Categories()
        # category.label = "Hobbies"
        # category.save()

    #     response = self.client.delete(f"/categories/{category.id}")
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     response = self.client.get(f"/categories/{category.id}")
    #     self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)