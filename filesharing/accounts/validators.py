from rest_framework import serializers

def check_len_password(value):
    if len(value.strip()) <= 8:
        raise serializers.ValidationError('Password length must be at least 8 characters.')
    return value