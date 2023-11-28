import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import Tags

class TagsTests(APITestCase):

    fixtures = ['tags', 'users', 'tokens']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_create_tags(self):
        url = "/tags"

        data = {
            "label": "Hobbies"
        }
        response = self.client.post(url, data, format='json')
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response["label"], "Hobbies")
        self.assertEqual(json_response["id"], 21)

    def test_get_tags(self):
        tags = Tags()
        tags.label = "Hobbies"
        tags.save()

        response = self.client.get(f"/tags/{tags.id}")
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Hobbies")
        self.assertEqual(json_response["id"], 21)
        
    def test_change_tags(self):
        tags = Tags()
        tags.label = "Hobbies"
        tags.save()

        data = {
            "label": "Wellness"
        }
        response = self.client.put(f"/tags/{tags.id}", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/tags/{tags.id}")
        json_response = json.loads(response.content)  
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["label"], "Wellness")

    def test_delete_tag(self):
        tags = Tags()
        tags.label = "Politics"
        tags.save()

        response = self.client.delete(f"/tags/{tags.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        response = self.client.get(f"/tags/{tags.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)