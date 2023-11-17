from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rareapi.models import RareUsers

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    '''Handles the authentication of a user

    Method arguments:
      request -- The full HTTP request object
    '''
    email = request.data['email']
    password = request.data['password']

    # Use the built-in authenticate method to verify
    # authenticate returns the user object or None if no user is found
    authenticated_user = authenticate(username=email, password=password)

    # If authentication was successful, respond with their token
    if authenticated_user is not None:
        token = Token.objects.get(user=authenticated_user)
        data = {
            'valid': True,
            'token': token.key
        }
        return Response(data)
    else:
        # Bad login details were provided. So we can't log the user in.
        data = { 'valid': False }
        return Response(data)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    '''Handles the creation of a new gamer for authentication

    Method arguments:
      request -- The full HTTP request object
    '''

    # Create a new user by invoking the `create_user` helper method
    # on Django's built-in User model
    new_user = User.objects.create_user(
        username=request.data['email'],
        password=request.data['password'],
        first_name=request.data['first_name'],
        last_name=request.data['last_name']
    )

    new_rare_user = RareUsers()
    new_rare_user.user_id = new_user.id
    new_rare_user.bio = request.data.get('bio')
    new_rare_user.profile_image_url = request.data.get('profile_image_url')
    new_rare_user.save()
    # Use the REST Framework's token generator on the new user account
    token = Token.objects.create(user=new_user)
    # Return the token to the client
    data = { 'token': token.key }
    return Response(data)