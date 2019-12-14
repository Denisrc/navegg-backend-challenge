from rest_framework import serializers
from sites.models import Sites

class SitesSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    active = serializers.BooleanField(required=False)
    url = serializers.CharField(required=True)
    category = serializers.CharField(required=True)

    def create(self, validated_data):
        return Sites.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.url = validated_data.get('url', instance.url)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance