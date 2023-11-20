from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rareapi.models import Comments, Posts, RareUsers


class CommentAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = RareUsers
        fields = ('user',)

class CommentPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('title',)

class CommentSerializer(serializers.ModelSerializer):
    post = CommentPostSerializer(many=False)
    author = CommentAuthorSerializer(many=False)
    class Meta:
        model = Comments
        fields = ('id', 'post', 'author', 'content', 'created_on')

class CommentView(viewsets.ViewSet):
    def list(self, request):
        comments = Comments.objects.all().order_by('created_on')
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        """Handle GET requests for single type

        Returns:
            Response -- JSON serialized type record
        """

        comment = Comments.objects.get(pk=pk)
        serialized = CommentSerializer(comment)
        return Response(serialized.data, status=status.HTTP_200_OK)