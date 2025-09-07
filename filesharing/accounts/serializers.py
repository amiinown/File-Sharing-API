from rest_framework import serializers
from .models import User
from .validators import check_len_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username', 'password')
        extra_kwargs = {
            'email': {'required':True},
            'username': {'required':True},
            'password': {'write_only':True, 'required':True, 'validators':(check_len_password,),}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
    
class ResetPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordConfirmSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True, validators=(check_len_password,))

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance