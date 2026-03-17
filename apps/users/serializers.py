from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    username = serializers.CharField(max_length=50, required=False)
    full_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField()
    disabled = serializers.BooleanField(default=False)