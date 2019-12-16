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

    def handle_reference(self, instance, reference_instance, data_list):
        for data in data_list:
            description = data['description']
            if not reference_instance.objects.filter(description=description).exists():
                reference_object = reference_instance.objects.create(description=description)
            else:
                reference_object = reference_instance.objects.get(description=description)

            if reference_instance.__name__ == 'SiteCategory':
                instance.category.add(reference_object)
            elif reference_instance.__name__ == 'SiteURL':
                instance.url.add(reference_object)

    def create(self, validated_data):
        site = Sites()
        site.name = validated_data['name']
        site.save()
        errors = { 'errors': []}
        if 'url' in validated_data:
            site.url.clear()
            request_urls = validated_data.pop('url')
            if len(request_urls) == 0:
                errors['errors'].append({'url': 'At least one URL is required'})
            else:
                self.handle_reference(site, SiteURL, request_urls)

        if 'category' in validated_data:
            site.category.clear()
            request_categories = validated_data.pop('category')
            if len(request_categories) == 0:
                errors['errors'].append({'category': 'At least one Category is required'})
            else:
                self.handle_reference(site, SiteCategory, request_categories)

        if len(errors['errors']) > 0:
            site.delete()
            raise serializers.ValidationError(errors)
        
        site.save()
        return site

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.save()

        if 'url' in validated_data:
            instance.url.clear()
            request_urls = validated_data.pop('url')
            self.handle_reference(instance, SiteURL, request_urls)

        if 'category' in validated_data:
            instance.category.clear()
            request_categories = validated_data.pop('category')
            self.handle_reference(instance, SiteCategory, request_categories)

        instance.save()

        return instance