import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import RareUsers

class RareUsersTests(APITestCase):

    fixtures = ['users', 'tokens', 'rare_users']

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUsers.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_get_rare_user(self):

        response = self.client.get(f"/users/{self.rare_user.id}")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["bio"], "I'm just like some guy, you know.")
        self.assertEqual(json_response["profile_image_url"], "https://pbs.twimg.com/profile_images/1279103276055539712/6pcd9iFM_400x400.jpg")
        self.assertEqual(json_response["created_on"], "2023-11-15T18:00:00Z")
        self.assertEqual(json_response["active"], True)
        self.assertEqual(json_response["rare_username"], "Cool Guy")
        self.assertEqual(json_response["user"]["full_name"], "Carrie Belk")
        self.assertEqual(json_response["user"]["email"], "me@me.com")
        self.assertEqual(json_response["user"]["is_staff"], "False")

    def test_get_rare_users(self):


        response = self.client.get("/users")

        json_response = json.loads(response.content)

        self.assertEqual(json_response[0]["bio"], "I'm just like some guy, you know.")
        self.assertEqual(json_response[0]["profile_image_url"], "https://pbs.twimg.com/profile_images/1279103276055539712/6pcd9iFM_400x400.jpg")
        self.assertEqual(json_response[0]["created_on"], "2023-11-15T18:00:00Z")
        self.assertEqual(json_response[0]["active"], True)
        self.assertEqual(json_response[0]["rare_username"], "Cool Guy")
        self.assertEqual(json_response[0]["user"]["full_name"], "Carrie Belk")
        self.assertEqual(json_response[0]["user"]["email"], "me@me.com")
        self.assertEqual(json_response[0]["user"]["is_staff"], "False")

        self.assertEqual(json_response[1]["bio"], "I'm Pajama Sam")
        self.assertEqual(json_response[1]["profile_image_url"], "https://pbs.twimg.com/profile_images/1279103276055539712/6pcd9iFM_400x400.jpg")
        self.assertEqual(json_response[1]["created_on"], "2023-11-10T14:00:00Z")
        self.assertEqual(json_response[1]["active"], True)
        self.assertEqual(json_response[1]["rare_username"], "Pajama Sam")
        self.assertEqual(json_response[1]["user"]["full_name"], "Admina Straytor")
        self.assertEqual(json_response[1]["user"]["email"], "admina@straytor.com")
        self.assertEqual(json_response[1]["user"]["is_staff"], "True")


