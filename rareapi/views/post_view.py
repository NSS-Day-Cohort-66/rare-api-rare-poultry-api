from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from django.utils import timezone
from rareapi.models import Posts, Comments, RareUsers


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('id', 'user', 'title', 'image_url', 'approved', 'category', 'content', 'tags' )

class UserSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField()

    def get_author_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    class Meta:
        model = User
        fields = ('author_name',)

class RareUsersSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False)  

    class Meta:
        model = RareUsers
        fields = ('id', 'user',)


class CommentsSerializer(serializers.ModelSerializer):
    author = RareUsersSerializer(many=False)

    class Meta:
        model = Comments
        fields = ('id', 'content', 'created_on', 'author',)


class PostSerializer(serializers.ModelSerializer):
    user = RareUsersSerializer(many=False)
    category_name = serializers.CharField(source='category.label', read_only=True)
    comments = CommentsSerializer(many=True)

        # Declare that an ad-hoc property should be included in JSON
    is_owner = serializers.SerializerMethodField()

    # Function containing instructions for ad-hoc property
    def get_is_owner(self, obj):
        # Check if the authenticated user is the owner
        return self.context['request'].user.id == obj.user_id

    class Meta:
        model = Posts
        fields = ('id', 'user', 'category_name', 'title', 'publication_date', 'image_url', 'content', 'approved', 'tags', 'comments', 'is_owner',)


class PostView(ViewSet):
    def list(self, request):
        posts = Posts.objects.filter(approved=True, publication_date__lte=timezone.now()).order_by('-publication_date')
        serialized = PostSerializer(posts, many=True, context={'request': request})
        return Response(serialized.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            single_post = Posts.objects.get(pk=pk)
            post_serialized = PostSerializer(single_post, context={'request': request})
            return Response(post_serialized.data)
        except Posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        title = request.data.get('title')
        publication_date = request.data.get('publication_date')
        image_url = request.data.get('image_url')
        category_id = request.data.get('category')
        content = request.data.get('content')

        post = Posts.objects.create(
            user=request.user.rareusers,
            title=title,
            publication_date=publication_date,
            image_url=image_url,
            category_id=category_id,
            content=content,
            approved=True)
        
        tags_ids = request.data.get('tags', [])
        post.tags.set(tags_ids)

        serializer = PostSerializer(post, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, pk=None):
        try:
            post = Posts.objects.get(pk=pk)
            serializer = PostUpdateSerializer(post, data=request.data, context={'request': request})
            if serializer.is_valid():
                post.user = serializer.validated_data['user']
                post.title = serializer.validated_data['title']
                post.image_url = serializer.validated_data['image_url']
                post.category_id = serializer.validated_data['category']
                post.content = serializer.validated_data['content']
                post.approved = serializer.validated_data['approved']
                post.save()
                tags_ids = request.data.get('tags', [])
                post.tags.set(tags_ids)
                serializer = PostUpdateSerializer(post, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

                
    
        except Posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
    
    def destroy(self, request, pk=None):
        try:
            post = Posts.objects.get(pk=pk)
            post.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Posts.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)