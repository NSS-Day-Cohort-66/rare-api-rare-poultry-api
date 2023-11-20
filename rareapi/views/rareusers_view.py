"""View module for handling requests about rare_users"""
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django.contrib.auth.models import User
from rareapi.models import RareUsers


class RareUsersView(ViewSet):
    """Viewset for rare_users"""

    def retrieve(self, request, pk=None):
        """Handle GET requests for single game

        Returns:
            Response -- JSON serialized game instance
        """
        rare_user = RareUsers.objects.get(pk=pk)
        serialized = RareUsersSerializer(rare_user)
        return Response(serialized.data)


    def list(self, request):
        """Handle GET requests to rare_users resource

        Returns:
            Response -- JSON serialized list of rare_users
        """
        rare_users = RareUsers.objects.all()
        serialized = RareUsersSerializer(rare_users, many=True)
        return Response(serialized.data)

class UserRareUsersSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()

    def get_email(self, obj):
        return f'{obj.username}'

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'

    class Meta:
        model = User
        fields = ('full_name', 'email',)

class RareUsersSerializer(serializers.ModelSerializer):
    
    user = UserRareUsersSerializer(many=False)

    class Meta:
        model = RareUsers
        fields = ('bio', 'profile_image_url', 'created_on', 'active', 'rare_username', 'user',)
