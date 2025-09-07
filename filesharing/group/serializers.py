from rest_framework import serializers
from .models import Group, UserGroupPermission
from accounts.models import User


class GroupAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)
        extra_kwargs = {
            'name' : {'required':True}
        }

    def validate_name(self, value):
        value = value.strip()
        user = self.context['request'].user
        same_group = Group.objects.filter(owner=user, name=value)
        if same_group.exists():
            raise serializers.ValidationError('This name does exists for another group.')
        
        return value
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner'] = user
        return super().create(validated_data)
    
class GroupListSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')
    permission = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ('id', 'name', 'owner', 'permission')

    def get_permission(self, obj):
        user = self.context['request'].user

        if user == obj.owner:
            return 'owner'
        
        try:
            user_permission = obj.user_permissions.get(user=user)
            return user_permission.get_permission_display()
        except UserGroupPermission.DoesNotExist:
            return 'Permission Not found.'

class GroupMemberPermissionSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, slug_field='username')
    permission = serializers.CharField(source="get_permission_display")  # برای نمایش متن انتخابی مثل "Read & Write"

    class Meta:
        model = UserGroupPermission
        fields = ('user', 'permission')

class GroupListMembersSerializer(serializers.ModelSerializer):
    members = GroupMemberPermissionSerializer(source='user_permissions', many=True)
    owner = serializers.SlugRelatedField(read_only=True, slug_field='username')
    class Meta:
        model = Group
        fields = ('owner', 'members',)

class GroupAddMembersSerializer(serializers.ModelSerializer):
    user_name = serializers.SlugRelatedField(
        required=True,
        queryset=User.objects.all(),
        slug_field='username',
        source = 'user',
        error_messages={
            'does_not_exist': 'There is no such user.',
        }
    )

    class Meta:
        model = UserGroupPermission
        fields = ('user_name','permission')
        extra_kwargs = {
            'permission': {'required':True}
        }

    def validate_user_name(self, value):
        user = value
        group = self.context['group']
        if group.owner == user:
            raise serializers.ValidationError('The group owner can not be add as a member.')

        if UserGroupPermission.objects.filter(user=user, group=group).exists():
            raise serializers.ValidationError('This user is already a member of this group.')
        
        return value
        
    def create(self, validated_data):
        group = self.context['group']
        return UserGroupPermission.objects.create(group=group ,**validated_data)

class GroupDeleteMembersSerializer(serializers.ModelSerializer):
    user_name = serializers.SlugRelatedField(
        required=True,
        queryset=User.objects.all(),
        slug_field='username',
        source = 'user',
        error_messages={
            'does_not_exist': 'There is no such user.',
        }
    )

    class Meta:
        model = UserGroupPermission
        fields = ('user_name',)

    def validate_user_name(self, value):
        user = value
        group = self.context['group']

        is_group_member = UserGroupPermission.objects.filter(user=user, group=group)
        if not is_group_member.exists():
            raise serializers.ValidationError('User is not a member of the current group.')
        
        return value
    
    def delete(self, validated_data):
        user = validated_data['user']
        group = self.context['group']
        
        try:
            user_permission = UserGroupPermission.objects.get(user=user, group=group)
            user_permission.delete()
        except UserGroupPermission.DoesNotExist:
            raise serializers.ValidationError('User not found in the group.')
        
class GroupChangeMemberPermissionSerializer(serializers.ModelSerializer):
    user_name = serializers.SlugRelatedField(
        required=True,
        queryset=User.objects.all(),
        slug_field='username',
        source='user',
        error_messages={
            'does_not_exist': 'There is no such user.',
        }
    )

    class Meta:
        model = UserGroupPermission
        fields = ('user_name', 'permission')
        extra_kwargs = {
            'permission':{'required':True}
        }

    def validate_user_name(self, value):
        user = value
        group = self.context['group']
        if not UserGroupPermission.objects.filter(user=user, group=group).exists():
            raise serializers.ValidationError('This user is not a member of the group.')
        return value

    def update(self, instance, validated_data):
        instance.permission = validated_data.get('permission', instance.permission)
        instance.save()
        return instance
