from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rareapi.models import Comments

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('id', 'post', 'author', 'content', 'created_on')

class CommentView(viewsets.ViewSet):
    def list(self, request):
        comments = Comments.objects.all().order_by('created_on')
        serialized = CommentSerializer(comments, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    