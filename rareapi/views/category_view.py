from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Categories

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for types"""
    class Meta:
        model = Categories
        fields = ('id', 'label', )

class CategoryView(ViewSet):
    def list(self, request):
        """Handle GET requests to get all Categories
        
        Returns:
            response -- JSON serialized list of types
        """

        categories = Categories.objects.all().order_by('label')
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            serialized = CategorySerializer(category)
            return Response(serialized.data, status=status.HTTP_200_OK)
        except Categories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def create(self, request):
        category = Categories()
        category.label = request.data['label']
        category.save()

        serialized = CategorySerializer(category, many=False)
        return Response(serialized.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            serializer = CategorySerializer(data=request.data)
            if serializer.is_valid():
                category.label = serializer.validated_data['label']
                category.save()
                serializer = CategorySerializer(category, context={'request': request})
                return Response(None, status.HTTP_204_NO_CONTENT)
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        
        except Categories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def destroy(self, request, pk=None):
        try:
            category = Categories.objects.get(pk=pk)
            category.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Categories.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
