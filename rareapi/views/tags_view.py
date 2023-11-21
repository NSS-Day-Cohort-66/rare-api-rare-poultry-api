from rest_framework import viewsets, serializers, status
from rest_framework.response import Response
from rareapi.models import Tags

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tags
        fields = ('id', 'label',)

class TagView(viewsets.ViewSet):
    # List many tags
    def list(self, request): 
        tags = Tags.objects.all().order_by('label')
        serialized = TagSerializer(tags, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    # List one tag
    def retrieve(self, request, pk=None):
        tag = Tags.objects.get(pk=pk)
        serialized = TagSerializer(tag)
        return Response(serialized.data, status=status.HTTP_200_OK)
    # Create a tag
    def create(self, request):
        tag = Tags()
        tag.label = request.data['label']
        tag.save()

        serialized = TagSerializer(tag, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)
    # Edit a tag
    def update(self, request, pk=None):
        try:
            tag = Tags.objects.get(pk=pk)
            serializer = TagSerializer(data=request.data)
            # Serialize the request data to check validity of the request, if not return an error
            if serializer.is_valid():
                tag.label = serializer.validated_data['label']
                tag.save()
                serializer = TagSerializer(tag, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

        except Tags.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)