from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True)
    price = serializers.FloatField()
    stock = serializers.IntegerField(default=0)