from django.contrib.auth.models import User
from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rareapi.models import Comments, Posts, RareUsers

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'post', 'author', 'content',)

class CommentsView(viewsets.ViewSet):

    def update(self, request, pk=None):
        try:
            comment = Comments.objects.get(pk=pk)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                comment.content = serializer.validated_data['content']
                comment.save()
                serializer = CommentSerializer(comment, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Comments.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


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