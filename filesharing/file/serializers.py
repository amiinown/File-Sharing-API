from rest_framework import serializers
from .models import File
from folder.models import Folder


class FileSerializer(serializers.ModelSerializer):
    uploaded_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M')
    owner = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = ('id', 'title', 'original_name', 'version', 'uploaded_at', 'owner')

    def get_owner(self, obj):
        if obj.group:
            return obj.owner.username
        return None



def validate_file_size(value):
    max_size = 10 * 1000 * 1000 # 10 MB
    if value.size > max_size:
        raise serializers.ValidationError('The Size of uploaded file must be lower or equel than 10 MB.')
    return value

class FileAddSerializer(serializers.ModelSerializer):
    folder = serializers.PrimaryKeyRelatedField(
        queryset=Folder.objects.all(),
        allow_null=True,
        required=False,
        error_messages={
            'invalid': 'Folder ID must be an integer.',
            'does_not_exist': 'There is no such folder.',
            'incorrect_type': 'folder field must be a folder integer ID.',
        }
    )
    uploaded_file = serializers.FileField(
        required=True,
        validators=[validate_file_size],
    )

    class Meta:
        model = File
        fields = ('title', 'folder', 'uploaded_file')
        extra_kwargs = {
            'title':{'required':True,},
        }
    
    def validate_folder(self, value):
        user = self.context['request'].user
        if value is not None and value.owner != user:
            raise serializers.ValidationError('There is no such folder.')
        return value
    
    def create(self, validated_data):
        validated_data['owner'] = self.context['owner']
        validated_data['group'] = self.context['group']
        validated_data['original_name'] = validated_data['uploaded_file'].name
        return File.objects.create(**validated_data)