from rest_framework import serializers
from sites.models import Sites, SiteCategory, SiteURL

class SiteCategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=True, max_length=100)   

    def create(self, validated_data):
        return SiteCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.name)
        instance.save()
        return instance

    class Meta:
        model = SiteCategory
        fields = ['id', 'description']

class SiteURLSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    description = serializers.CharField(required=True, max_length=100)

    def create(self, validated_data):
        return SiteURL.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.description = validated_data.get('description', instance.name)
        instance.save()
        return instance

    class Meta:
        model = SiteURL
        fields = ['id', 'description']

class SitesSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, max_length=100)
    active = serializers.BooleanField(required=False)
    url = SiteURLSerializer(many=True)
    category = SiteCategorySerializer(many=True)

    class Meta:
        model = Sites
        fields = ['id', 'name', 'url', 'category', 'active']