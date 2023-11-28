import json
from rest_framework import status
from rest_framework.test import APITestCase

class AuthorizationTests(APITestCase):

    fixtures = ['users', 'tokens']

    def test_login(self):
        url = '/login'

        data = {
            "email": "me@me.com",
            "password": "me"
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["valid"], True)
        self.assertEqual(json_response["token"], "fa2eba9be8282d595c997ee5cd49f2ed31f65bed")

class RegisterTests(APITestCase):

    fixtures = ['users', 'tokens']

    def test_register_user(self):
        url='/register'

        data = {
            'email': 'me2@me.com',
            'password': 'me2',
            'first_name': 'Paolo',
            'last_name': 'Medel',
            'bio': 'im me2',
            'profile_image_url': 'here is url',
            'rare_username': 'me2@me.com'
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertIsNotNone(json_response["token"])
     