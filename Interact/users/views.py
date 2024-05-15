from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import generics

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from .models import Profile, ProfileGithub
from .serializers import ProfileSerializer, ProfileGithubSerializer
from api.permissions import IsOwner


@api_view(['POST'])
def obtain_token(request):
    if request.method == 'POST':
        data = request.data
        username = data.get('username')
        password = data.get('password')
        if username and password:
            user = get_object_or_404(User, username=username)
            user = authenticate(request, username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                detail = {
                    "detail": f'Here is your Token: {token.key}'
                }
                return Response(detail)

            detail = {
            "detail": "No User matches the given query."
            }
            return Response(detail)


        detail = {
            "Bad Response, Not valid information."
        }
        return Response(detail)


class ProfileListGenericAPIView(generics.ListAPIView):
    queryset = ProfileGithub.objects.all()
    serializer_class = ProfileGithubSerializer
    # permission_classes = [permissions.IsAuthenticated & permissions.IsAdminUser]

list_profile_generic = ProfileListGenericAPIView.as_view()



class ProfileRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsOwner)]
    lookup_field = 'username'

retrieve_profile_generic = ProfileRetrieveAPIView().as_view()



@api_view(['POST'])
def create_profile(request):
    if request.method == 'POST':
        data = request.data
        serializer = ProfileGithubSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save() 
            
            return Response(serializer.data)




# @api_view(['POST'])
# def create_profile(request):
#     if request.method == 'POST':
#         context = {'request': request}


#         username = request.data.get('username').lower()
#         password = request.data.get('password')
#         email = request.data.get('email')

#         if User.objects.filter(username=username):
#             detail = {
#                 'detail': 'This name is used before.'
#             }
#             return Response(detail)

#         user = User.objects.create(
#             username= username,
#             email=email,
#         )
#         user.set_password(password)
#         user.save()

#         data = request.data
#         data['owner'] = user.pk
        
        
#         serializer = ProfileSerializer(data=data, context=context)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response(serializer.data)


class ProfileDeleteGenericAPIView(generics.DestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    lookup_field = 'username'

delete_profile_generic = ProfileDeleteGenericAPIView.as_view()    
