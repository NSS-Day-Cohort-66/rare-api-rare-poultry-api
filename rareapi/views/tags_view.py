from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rareapi.models import Tags

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'label',)

class TagView(viewsets.ViewSet):
    def list(self, request):
        tags = Tags.objects.all()
        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)