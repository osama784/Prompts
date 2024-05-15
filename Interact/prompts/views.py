from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import permissions
from rest_framework import status

from django.shortcuts import get_object_or_404

from .models import Prompt
from users.models import Profile, ProfileGithub
from .serializers import PromptSerializer, PromptSerializerShow, PromptSerializerShowRestricted
from api.permissions import PromptsPermission, IsOwner
from api.mixins import UserQuerysetMixin


#Listing Prompts:
@api_view(['GET'])
def list_prompts(request):
    context = {'request': request}
    prompts = Prompt.objects.all()
    data = PromptSerializer(prompts, many=True, context=context).data

    return Response(data)



class PromptGenericListAPIView(generics.ListAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializerShowRestricted
    
prompt_list_generic = PromptGenericListAPIView().as_view()


#Retrieve Prompts:

@api_view(['GET'])
def retrieve_prompt(request, prompt_pk):
    prompt = Prompt.objects.get(pk=prompt_pk)
    data = PromptSerializerShowRestricted(prompt).data

    return Response(data)



class PromptGenericRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializerShowRestricted
    lookup_field = 'pk'

prompt_retrieve_generic = PromptGenericRetrieveAPIView().as_view()



#Create Prompts:


@api_view(['POST'])
def create_prompt(request):
    # if request.method == 'POST':
        context = {'request': request}
        data = request.data
        email = data.get('email')
        profile = ProfileGithub.objects.filter(email=email).first()
        data.pop('email')
        data['owner'] = profile.pk
        print(data)
        serializer = PromptSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        

@api_view(['POST'])
def get_proifle_prompts(request):
    if request.method == "POST":
        data = request.data

        email = data.get('email')
        if not email:
            prompts = Prompt.objects.all()
            serializer = PromptSerializer(prompts, many=True)
            return Response(serializer.data)
        
        profile = ProfileGithub.objects.filter(email=email).first()
        prompts = profile.prompt_set.all()
        if not prompts:
            detail = {
                'detail': 'No prompts available'
            }
            return Response(detail)
        serializer = PromptSerializer(prompts, many=True)
        return Response(serializer.data)
    detail  = {
        'detail': 'meow'
    }
    return Response(detail)


@api_view(['PATCH'])
def update_prompt(requset, id):
    if requset.method == "PATCH":
        data = requset.data
        prompt = Prompt.objects.get(pk=id)
        profile = prompt.owner
        data['owner'] = profile.pk
        print(prompt)
        serializer = PromptSerializer(instance=prompt, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        

@api_view(['DELETE'])
def delete_prompt(request, id):
    if request.method == 'DELETE':
        prompt = Prompt.objects.get(pk=id)
        prompt.delete()
        detail = {
            'detail': 'Prompt deleted'
        }
        return Response(detail)




# @api_view(['POST', 'GET'])
# @permission_classes([permissions.IsAuthenticated])
# def create_prompt(request):
#     if request.method == 'POST':
#         context = {'request': request}
#         data = request.data
#         data['owner'] = request.user.profile.pk
#         serializer = PromptSerializer(data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             # data = serializer.data
#             instance = serializer.instance
#             data = PromptSerializerShow(instance, context=context).data
#             return Response(data)
#     return Response({'detail': 'Create a prompt before trying to get data'})    



class PromptGenericCreateAPIView(generics.CreateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

        
    #     self.perform_create(serializer)

    #     context = {'request': request}
    #     instance = serializer.instance
    #     data = PromptSerializerShow(instance, context=context).data

    #     headers = self.get_success_headers(serializer.data)
    #     return Response(data, status=status.HTTP_201_CREATED, headers=headers)

prompt_create_generic = PromptGenericCreateAPIView.as_view()


#Delete Prompt:
# @api_view(['DELETE', 'GET'])
# @permission_classes([permissions.IsAuthenticated])
# def delete_prompt(request, prompt_pk):
#     prompt = get_object_or_404(Prompt, pk=prompt_pk)
    
#     if request.method == 'DELETE':
#         check = PromptsPermission.check_owner(self=None, request=request, obj=prompt)
#         if not check:
#             detail = {
#                 "detail": "You do not have permission to perform this action."
#             }
#             return Response(detail)
#         prompt.delete()
#         return Response({'detail': f'Prompt {prompt_pk} Deleted Successfully!'})
    
#     data = PromptSerializer(prompt).data
#     return Response(data)



class PromptGenericDeleteAPIView(generics.DestroyAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer
    permission_classes = [permissions.IsAuthenticated, (permissions.IsAdminUser | IsOwner)]
    lookup_field = 'pk'

    def destroy(self, request, *args, **kwargs):
        
        instance = self.get_object()
        pk = instance.pk
        self.perform_destroy(instance)
        return Response({'detail': f'Prompt {pk} Deleted Successfully!'})
    
    

prompt_delete_generic = PromptGenericDeleteAPIView.as_view()    


#Update Prompt:
# @api_view(['PUT', 'GET'])
# def update_promp(request, prompt_pk):
#     prompt = get_object_or_404(Prompt, pk=prompt_pk)
#     if request.method == 'PUT':
#         data = request.data
#         serializer = PromptSerializer(prompt, data=data)
#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
#             return Response({'message': 'Prompt Updated Successfully!'})
#     data = PromptSerializer(prompt).data
#     return Response(data)    



class PromptGenericUpdateAPIView(generics.UpdateAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

    def update(self, request, *args, **kwargs):
        pk = kwargs.pop('pk')
        prompt = get_object_or_404(Prompt, pk=pk)
        serializer = PromptSerializer(prompt, data=request.data) 
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': f'Prompt {pk} Updated Successfully!'})
    

prompt_update_generic = PromptGenericUpdateAPIView.as_view()



#Prompts for specific user

@api_view(['GET'])
def profile_prompts(request, username):
    profile = get_object_or_404(Profile, username=username)
    prompts = profile.prompt_set.all()
    context = {'request': request}
    data = PromptSerializer(prompts, many=True, context=context).data
    return Response(data)


class PromptsUserGenericAPIView(generics.ListAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

    def list(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, username=kwargs.get('username'))
        kwargs.pop('username')
        qs = super().get_queryset(*args, **kwargs)
        serializer = self.get_serializer(qs.filter(owner=profile), many=True)
        return Response(serializer.data)
        
    
                    

prompts_user_generic = PromptsUserGenericAPIView.as_view()


#Another way for listing prompts depending on the user

class PromptGenericListAPIViewV3(
    UserQuerysetMixin,
    generics.ListAPIView):
    queryset = Prompt.objects.all()
    serializer_class = PromptSerializer

    user_field = 'owner'
    # allow_staff_view = True


prompt_list_generic_v3 = PromptGenericListAPIViewV3().as_view()