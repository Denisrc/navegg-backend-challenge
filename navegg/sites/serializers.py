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
        fields = ['id', 'name', 'active', 'url', 'category']

    # Create the category or url for the sites if necessary
    def handle_reference(self, instance, reference_instance, data_list):
        for data in data_list:
            description = data['description']
            # Verify if the category or url already exists, if not exists create a new
            # if exist find the object
            if not reference_instance.objects.filter(description=description).exists():
                reference_object = reference_instance.objects.create(description=description)
            else:
                reference_object = reference_instance.objects.get(description=description)

            # Add the searched/created object to the Site reference
            if reference_instance.__name__ == 'SiteCategory':
                instance.category.add(reference_object)
            elif reference_instance.__name__ == 'SiteURL':
                instance.url.add(reference_object)

    def create(self, validated_data):
        site = Sites()
        site.name = validated_data['name']
        if 'active' in validated_data:
            site.active = validated_data['active']

        # Save the site to be able to link the category and url to the site
        site.save()
        errors = { 'errors': []}

        # Handle the url in the request
        if 'url' in validated_data:
            site.url.clear()
            request_urls = validated_data.pop('url')
            # Check if the request contains at least one url
            if len(request_urls) == 0:
                errors['errors'].append({'url': 'At least one URL is required'})
            else:
                self.handle_reference(site, SiteURL, request_urls)

        # Handle the category in the request
        if 'category' in validated_data:
            site.category.clear()
            request_categories = validated_data.pop('category')
            # Check if the request contains at least one category
            if len(request_categories) == 0:
                errors['errors'].append({'category': 'At least one Category is required'})
            else:
                self.handle_reference(site, SiteCategory, request_categories)

        if len(errors['errors']) > 0:
            # Delete the created site
            site.delete()
            raise serializers.ValidationError(errors)
        
        site.save()
        return site

    def update(self, instance, validated_data):
        instance.name = validated_data['name']
        instance.active = validated_data['active']
        instance.save()

        errors = { 'errors': []}

        if 'url' in validated_data:
            request_urls = validated_data.pop('url')

            # Check if the request contains at least one url
            if len(request_urls) == 0:
                errors['errors'].append({'url': 'At least one URL is required'})
            else:
                # Remove all urls related to this site before adding the
                # urls passed in the request
                instance.url.clear()
                self.handle_reference(instance, SiteURL, request_urls)

        if 'category' in validated_data:
            request_categories = validated_data.pop('category')

            # Check if the request contains at least one category
            if len(request_categories) == 0:
                errors['errors'].append({'category': 'At least one Category is required'})
            else:
                # Remove all categories related to this site before adding the
                # categories passed in the request
                instance.category.clear()
                self.handle_reference(instance, SiteCategory, request_categories)

        if len(errors['errors']) > 0:
            raise serializers.ValidationError(errors)

        instance.save()

        return instance