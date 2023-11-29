import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import Comments, RareUsers

class CommentsTests(APITestCase):

    fixtures = ['users', 'rare_users', 'tokens', 'posts', 'comments', 'categories', 'tags']

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUsers.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")

    def test_change_comments(self):
        comment = Comments()
        comment.post_id = 1
        comment.author_id = 1
        comment.content = "Original Comment"
        comment.save()

        data = {
            "post": 1,
            "author": 1,
            "content": "Edited Comment"
        }

        response = self.client.put(f"/comments/{comment.id}", data, format="json")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/comments/{comment.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["content"], "Edited Comment")

    def test_create_comment(self):
        data = {
            "post": 1,
            "author": self.rare_user.id,
            "content": "test"
        }

        response = self.client.post("/comments", data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json_response['post'], 1)
        self.assertEqual(json_response['author'], self.rare_user.id)
        self.assertEqual(json_response['content'], "test")
