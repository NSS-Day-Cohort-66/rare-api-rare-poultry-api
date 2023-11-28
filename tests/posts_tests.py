import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import Posts

class PostsTests(APITestCase):

    fixtures = ['users', 'tokens', 'posts']

    def setUp(self):
        self.user = User.objects.first()
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_create_posts(self):
        url = "/posts"

        data = {
            "user": self.user.id,
            "category": 1,
            "title": "New Test Post",
            "publication_date": "2022-11-11",
            "image_url": "www.testimage.jpeg",
            "content": "Here is the content for test post",
            "approved": True,
            "tags": [2, 4]
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["user"], self.user.id)
        self.assertEqual(json_response["category"], 1)
        self.assertEqual(json_response["title"], "New Test Post")
        self.assertEqual(json_response["publication_date"], "2022-11-11")
        self.assertEqual(json_response["image_url"], "www.testimage.jpeg")
        self.assertEqual(json_response["content"], "Here is the content for test post")
        self.assertEqual(json_response["approved"], True)
        self.assertEqual(json_response["tags"], [2, 4])


    # def test_get_posts(self):

    #     post - Post()


        
