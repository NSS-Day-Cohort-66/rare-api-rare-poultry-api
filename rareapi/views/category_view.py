from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rareapi.models import Categories

class CategoryView(ViewSet):
    def list(self, request):
        """Handle GET requests to get all Categories
        
        Returns:
            response -- JSON serialized list of types
        """

        categories = Categories.objects.all()
        serialized = CategorySerializer(categories, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)
    
    def retrieve(self, request, pk=None):
        category = Categories.objects.get(pk=pk)
        serialized = CategorySerializer(category)
        return Response(serialized.data, status=status.HTTP_200_OK)

class CategorySerializer(serializers.ModelSerializer):
    """JSON serializer for types"""
    class Meta:
        model = Categories
        fields = ('id', 'label', )
