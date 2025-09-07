from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsGroupOwner, IsGroupOwnerOrMember
from rest_framework.response import Response
from .models import Group, UserGroupPermission
from rest_framework import status, generics
from .serializers import (
    GroupAddSerializer, GroupListSerializer, GroupListMembersSerializer,
    GroupAddMembersSerializer, GroupDeleteMembersSerializer, GroupChangeMemberPermissionSerializer
)
from django.db.models import Q


GROUP_NOT_FOUND_MESSAGE = {'error':'Group Not found.'}


class GroupListAddView(generics.ListCreateAPIView):
    """
    List or create groups.

    get: 
        list user groups.

    post: 
        create a new group.
    """
    permission_classes = [IsAuthenticated]
    

    def get_queryset(self):
        user = self.request.user
        return Group.objects.filter(Q(owner=user) | Q(members=user))\
            .select_related('owner').prefetch_related('user_permissions').distinct()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return GroupAddSerializer
        return GroupListSerializer
        
class GroupDeleteView(generics.DestroyAPIView):
    """
    Remove group.
    """
    permission_classes = [IsAuthenticated, IsGroupOwner]
    lookup_url_kwarg = 'group_id'

    def get_queryset(self):
        return Group.objects.select_related('owner').all()
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(data={
            'message':'Group removed successfully.'
            }, status=status.HTTP_202_ACCEPTED)
        
class GroupListMembersView(APIView):
    """
    List members of the Group.
    """
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember]
    serializer_class = GroupListMembersSerializer

    def get(self, request, group_id):

        try:
            group = Group.objects.prefetch_related('members').get(pk=group_id)
            self.check_object_permissions(self.request, group)
            ser_group_members_data = GroupListMembersSerializer(instance=group).data
            return Response(data=ser_group_members_data, status=status.HTTP_200_OK)          
        except Group.DoesNotExist:
            return Response(data=GROUP_NOT_FOUND_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        
class GroupAddMembersView(APIView):
    """
    Add a user to group.
    """
    permission_classes = [IsAuthenticated, IsGroupOwner]
    serializer_class = GroupAddMembersSerializer

    def post(self, request, group_id):
        
        try:
            group = Group.objects.get(pk=group_id)
            self.check_object_permissions(self.request, group)
        except Group.DoesNotExist:
            return Response(data=GROUP_NOT_FOUND_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        
        ser_data = GroupAddMembersSerializer(data=request.data, context={'request':request, 'group':group})
            
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)

            return Response(data={
                'message':'The user added to group successfully.'
            }, status=status.HTTP_201_CREATED)
        
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupDeleteMembersView(APIView):
    """
    Remove a user from group.
    """
    permission_classes = [IsAuthenticated, IsGroupOwner]
    serializer_class = GroupDeleteMembersSerializer

    def delete(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
            self.check_object_permissions(self.request, group)
        except Group.DoesNotExist:
            return Response(data=GROUP_NOT_FOUND_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        
        ser_data = GroupDeleteMembersSerializer(data=request.data, context={'request':request, 'group':group})

        if ser_data.is_valid():
            ser_data.delete(ser_data.validated_data)

            return Response(data={
                'message':'The user removed from group successfully.'
            }, status=status.HTTP_204_NO_CONTENT)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
class GroupChangeMembersPermissionView(APIView):
    """
    Change user's permission by the Owner group.
    """
    permission_classes = [IsAuthenticated, IsGroupOwner]
    serializer_class = GroupChangeMemberPermissionSerializer
    
    def patch(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
            self.check_object_permissions(self.request, group)
        except Group.DoesNotExist:
            return Response(data=GROUP_NOT_FOUND_MESSAGE, status=status.HTTP_404_NOT_FOUND)
        
        ser_data = GroupChangeMemberPermissionSerializer(data=request.data, context={'request':request, 'group':group})

        if ser_data.is_valid():
            member = UserGroupPermission.objects.select_related('user').select_related('group')\
            .get(user=ser_data.validated_data['user'], group=group)

            ser_data.update(member, ser_data.validated_data)
            return Response(data={'message':'Permission updated successfully.'}, status=status.HTTP_202_ACCEPTED)
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)