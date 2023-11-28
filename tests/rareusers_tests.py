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
        self.assertEqual(json_response["rare_username"], "")
        self.assertEqual(json_response["user"]["full_name"], "Carrie Belk")
        self.assertEqual(json_response["user"]["email"], "me@me.com")
        self.assertEqual(json_response["user"]["is_staff"], "False")

    def test_get_rare_users(self):
        test_user = User.objects.create_user(
        username='test@test.com',
        password='abc123',
        first_name="Testy",
        last_name="Testerson"
    )
        test_rare_user = RareUsers()
        test_rare_user.user_id = test_user.id
        test_rare_user.bio = "Test Bio"
        test_rare_user.profile_image_url = "www.test.com"
        test_rare_user.rare_username = "McTester"
        test_rare_user.save()

        response = self.client.get("/users")

        json_response = json.loads(response.content)

        self.assertEqual


