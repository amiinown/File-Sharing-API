from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from common.permissions import IsGroupOwnerOrMember, IsGroupOwnerOrReadWriteMember
from rest_framework import status
from folder.models import Folder
from .models import File
from folder.serializers import FolderSerializer
from .serializers import FileSerializer, FileAddSerializer
from rest_framework.parsers import MultiPartParser, FormParser
import boto3
from django.conf import settings
from group.models import Group




class ListFileView(APIView):
    """
    Returns user/group files.
    """
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember]

    def get(self, request, group_id=None):
        filters = {}

        if group_id:
            try:
                group = Group.objects.prefetch_related('members').get(pk=group_id)
                self.check_object_permissions(self.request, group)
                filters['group'] = group
            except Group.DoesNotExist:
                return Response(data={'error':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            filters['owner'] = request.user
            filters['group'] = None
        folders = Folder.objects.select_related('owner', 'group').filter(**filters)
        root_files = File.objects.select_related('owner', 'group', 'folder').filter(**filters, folder__isnull=True)

        ser_folder_data = FolderSerializer(instance=folders, many=True).data
        ser_root_files_data = FileSerializer(instance=root_files, many=True).data
        return Response(data={
            'folders':ser_folder_data,
            'root_files':ser_root_files_data,
        }, status=status.HTTP_200_OK)
    
class AddFileView(APIView):
    """
    Add file for user/group.
    """
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember, IsGroupOwnerOrReadWriteMember]
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileAddSerializer

    def post(self, request, group_id=None):
        user = request.user

        if group_id:
            try:
                group = Group.objects.prefetch_related('members').get(pk=group_id)
                self.check_object_permissions(self.request, group)
            except Group.DoesNotExist:
                return Response(data={'error':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            group = None
        
        ser_data = FileAddSerializer(data=request.data, context={'request':request, 'group':group, 'owner':user})
        if ser_data.is_valid():
            ser_data.save()
            return Response(data={'message':'File added successfully.'}, status=status.HTTP_201_CREATED)
        else:
            return Response(data=ser_data.errors,status=status.HTTP_400_BAD_REQUEST
            )
        
class DeleteFileView(APIView):
    """
    delete user/group file.
    """
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember, IsGroupOwnerOrReadWriteMember]

    def delete(self, request, file_id, group_id=None):
        filters = {'pk':file_id}

        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                self.check_object_permissions(self.request, group)
                filters['group'] = group
            except Group.DoesNotExist:
                return Response(data={'error':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            filters['group'] = None

        try:
            file = File.objects.get(**filters)
        except File.DoesNotExist:
            return Response(data={
                'error':'File not found.'
                }, status=status.HTTP_404_NOT_FOUND)
        
        file_original_name = file.original_name
        file_version = file.version
        file.delete()

        return Response(
            {"message": f'The <{file_original_name}> v{file_version} file deleted successfully.'},
            status=status.HTTP_204_NO_CONTENT
        )

class DownloadFileView(APIView):
    """
    Generate a presigned url to download user/group file.
    """
    permission_classes = [IsAuthenticated, IsGroupOwnerOrMember]

    def get(self, request, file_id, group_id=None):
        filters = {'pk':file_id}

        if group_id:
            try:
                group = Group.objects.get(pk=group_id)
                self.check_object_permissions(self.request, group)
                filters['group'] = group
            except Group.DoesNotExist:
                return Response(data={'error':'Group not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            filters['group'] = None
        

        try:
            file = File.objects.get(**filters)
        except File.DoesNotExist:
            return Response(data={'erorr':'File not found.'}, status=status.HTTP_404_NOT_FOUND) 

        s3Client = boto3.client(
            's3',
            endpoint_url=settings.AWS_S3_ENDPOINT_URL,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

        presigned_url = s3Client.generate_presigned_url(
            'get_object',
            Params = {
                'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                'Key': str(file.uploaded_file)
            },
            ExpiresIn = 60 * 10 # 5 minutes
        )

        return Response(data={'url':presigned_url})