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
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_get_rare_user(self):
        # rare_user = RareUsers()
        # rare_user.bio = "Test Bio"
        # rare_user.profile_image_url = "Test URL"
        # rare_user.created_on = "2023-11-15T18:00:00Z"
        # rare_user.active = True
        # rare_user.rare_username = "Test Username"
        # rare_user.user.full_name = "Firstname Lastname"
        # rare_user.user.email = "test@test.com"
        # rare_user.user.is_staff = False

        # rare_user.save()

        response = self.client.get("/users/1")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response["bio"], "I'm just like some guy, you know.")
        self.assertEqual(json_response["profile_image_url"], "https://pbs.twimg.com/profile_images/1279103276055539712/6pcd9iFM_400x400.jpg")
        self.assertEqual(json_response["created_on"], "2023-11-15T18:00:00Z")
        self.assertEqual(json_response["active"], True)
        self.assertEqual(json_response["rare_username"], "")
        self.assertEqual(json_response["user"]["full_name"], "Carrie Belk")
        self.assertEqual(json_response["user"]["email"], "me@me.com")
        self.assertEqual(json_response["user"]["is_staff"], "False")



