from rest_framework import serializers
from file.serializers import FileSerializer
from folder.models import Folder
import re

class FolderSerializer(serializers.ModelSerializer):
    files = serializers.SerializerMethodField()
    sub_folders = serializers.SerializerMethodField()

    class Meta:
        model = Folder
        fields = ('id', 'name', 'created_at', 'files', 'sub_folders')

    def get_files(self, obj):
        if isinstance(obj, Folder):
            files = obj.files.filter()
            return FileSerializer(instance=files, many=True).data
        return []
    
    def get_sub_folders(self, obj):
        if isinstance(obj, Folder):
            sub_folders = obj.sub_folders.all()
            return FolderSerializer(instance=sub_folders, many=True).data
        return []
    
class AddFolderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder
        fields = ('name', 'parent')
        extra_kwargs = {
            'name' : {'required':True,},
            'parent' : {'required':False,},
        }

    def validate_name(self, value):
        regex_pattern = r'^[\w\s\-.,!?()]{1,50}$'
        if not re.match(regex_pattern, value.strip()):
            raise serializers.ValidationError('Invalid folder name.')
        return value.strip()

    def validate(self, data):
        user = self.context['request'].user
        name = data['name']
        parent = data.get('parent') 

        if Folder.objects.filter(name=name, owner=user, parent=parent).exists():
            raise serializers.ValidationError('Such folder already exists in this directory.')
        return data

    def create(self, validated_data):
        group = self.context.get('group')
        user = self.context['request'].user

        validated_data.update(
            {
                'owner':user,
                'group':group
            })
        return Folder.objects.create(**validated_data)