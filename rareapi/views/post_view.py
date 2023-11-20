from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.utils import timezone
from rareapi.models import Posts
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    class Meta:
        model = User
        fields = ('author_name',)


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(source='user', read_only=True)
    category_name = serializers.CharField(source='category.label', read_only=True)

    class Meta:
        model = Posts
        fields = ('id', 'author', 'category_name', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', )


class PostView(ViewSet):
    def list(self, request):
        posts = Posts.objects.filter(approved=True, publication_date__lte=timezone.now()).order_by('-publication_date')
        serialized = PostSerializer(posts, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

