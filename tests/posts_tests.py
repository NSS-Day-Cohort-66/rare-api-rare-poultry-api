import json
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rareapi.models import Posts, RareUsers

class PostsTests(APITestCase):

    fixtures = ['users', 'rare_users', 'categories', 'tokens', 'posts', 'tags']

    def setUp(self):
        self.user = User.objects.first()
        self.rare_user = RareUsers.objects.get(user=self.user)
        token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token.key}")


    def test_create_posts(self):
        url = "/posts"

        data = {
            "user": self.rare_user.id,
            "category": 1,
            "title": "New Test Post",
            "image_url": "http://www.testimage.jpeg",
            "content": "Here is the content for test post",
            "approved": True,
            "tags": [2, 4],
        }

        response = self.client.post(url, data, format='json')

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(json_response["user"]["id"], self.rare_user.id)
        self.assertEqual(json_response["category_name"], "Funny")
        self.assertEqual(json_response["title"], "New Test Post")
        self.assertEqual(json_response["image_url"], "http://www.testimage.jpeg")
        self.assertEqual(json_response["content"], "Here is the content for test post")
        self.assertEqual(json_response["approved"], True)
        self.assertEqual(json_response["tags"], [2, 4])
        self.assertEqual(json_response["comments"], [])


    def test_get_posts(self):

        posts = Posts()
        posts.user = self.rare_user
        posts.category_id = 1
        posts.title = "Different Post"
        posts.image_url = "http://www.differentimage.jpeg"
        posts.content = "Testing get posts"
        posts.approved = True
        posts.save()
        posts.tags.set([2, 3])

        response = self.client.get(f"/posts/{posts.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["user"]["id"], self.rare_user.id)
        self.assertEqual(json_response["category_name"], "Funny")
        self.assertEqual(json_response["title"], "Different Post")
        self.assertEqual(json_response["image_url"], "http://www.differentimage.jpeg")
        self.assertEqual(json_response["content"], "Testing get posts")
        self.assertEqual(json_response["approved"], True)
        self.assertEqual(json_response["tags"], [2, 3])
        self.assertEqual(json_response["comments"], [])


    def test_get_all_posts(self):
        response = self.client.get("/posts")

        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(json_response[0]["title"], "Sample Post Number Three")
        self.assertEqual(json_response[1]["title"], "Sample Post Number One")



    def test_change_posts(self):

        posts = Posts()
        posts.user_id = 1
        posts.category_id = 1
        posts.title = "Changed Post"
        posts.image_url = "http://www.differentimage.jpeg"
        posts.content = "Here is the content for changing a post"
        posts.approved = True
        posts.save()
        posts.tags.set([2, 3])

        data = {
            "title": "Test it",
            "content": "Wowie Zowie",
            "user": 1,
            "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f2/Feral_rooster_on_Kaua%CA%BBi.jpg",
            "category": 2,
            "approved": True,
            "tags": [1,2,3]
                }

        response = self.client.put(f"/posts/{posts.id}", data, format="json")
        print(response.content)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/posts/{posts.id}")
        json_response = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response["category_name"], "Lifestyle")
        self.assertEqual(json_response["title"], "Test it")
        self.assertEqual(json_response["image_url"], "https://upload.wikimedia.org/wikipedia/commons/f/f2/Feral_rooster_on_Kaua%CA%BBi.jpg")
        self.assertEqual(json_response["content"], "Wowie Zowie")
        self.assertEqual(json_response["approved"], True)
        self.assertEqual(json_response["tags"], [2,3,1])
    

    def test_delete_posts(self):

        posts = Posts()
        posts.user = self.rare_user
        posts.category_id = 1
        posts.title = "Changed Post"
        posts.image_url = "http://www.differentimage.jpeg"
        posts.content = "Here is the content for changing a post"
        posts.approved = True
        posts.save()
        posts.tags.set([2, 3])
        
        response = self.client.delete(f"/posts/{posts.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f"/posts/{posts.id}")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)












        
