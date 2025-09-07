from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Folder
from rest_framework import status
from .serializers import AddFolderSerializer
from group.models import Group



class AddFolderView(APIView):
    """
    Add folder for user/group.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddFolderSerializer

    def post(self, request, group_id=None):

        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                self.check_object_permissions(self.request, group)
            except Group.DoesNotExist:
                return Response(data={'error':'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            group = None
        
        ser_data = AddFolderSerializer(data=request.data, context={'request': request, 'group':group})
        
        if ser_data.is_valid():
            ser_data.create(ser_data.validated_data)
            return Response(data={'message': 'Folder added successfully.'}, status=status.HTTP_201_CREATED)
        
        return Response(data=ser_data.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteFolderView(APIView):
    """"
    Delete user/group folder.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, folder_id, group_id=None):
        user = request.user
        filters = {'owner':user}

        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                self.check_object_permissions(self.request, group)
            except Group.DoesNotExist:
                return Response(data={'error':'Group not found.'}, status=status.HTTP_404_NOT_FOUND)
        else:
            group = None

        filters.update({
            'pk':folder_id,
            'group':group
        })

        try:
            folder = Folder.objects.get(**filters)
        except Folder.DoesNotExist:
            return Response(data={'error': 'There is no folder with this ID.'},
                status=status.HTTP_404_NOT_FOUND
            )

        folder_name = folder.name
        folder.delete()

        return Response(
            {"message": f'The <{folder_name}> folder deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )