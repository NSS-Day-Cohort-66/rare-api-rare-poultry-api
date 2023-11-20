from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rareapi.models import Tags

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'label',)

class TagView(viewsets.ViewSet):
    def list(self, request):
        tags = Tags.objects.all().order_by('label')
        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        tag = Tags.objects.get(pk=pk)
        serialized = TagSerializer(tag)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        tag = Tags()
        tag.label = request.data['label']
        tag.save()

        serialized = TagSerializer(tag, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)