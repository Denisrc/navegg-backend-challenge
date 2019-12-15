from django.shortcuts import render
from django.http import Http404
from sites.models import Sites, SiteURL, SiteCategory
from sites.serializers import SitesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class SitesList(APIView):

    def get(self, request, format=None):
        sites = Sites.objects.all()
        serializer = SitesSerializer(sites, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request_data = request.data
        request_urls = request_data.pop('url')
        # url.add
        site = Sites()
        site.name = request_data['name']
        site.save()
        for request_url in request_urls:
            description = request_url['description']
            if not SiteURL.objects.filter(description=description).exists():
                site_url = SiteURL.objects.create(description=description)
            else:
                site_url = SiteURL.objects.get(description=description)

            site.url.add(site_url)

        request_categories = request_data.pop('category')
        for request_category in request_categories:
            description = request_category['description']
            if not SiteCategory.objects.filter(description=description).exists():
                category_url = SiteCategory.objects.create(description=description)
            else:
                category_url = SiteCategory.objects.get(description=description)

            site.category.add(category_url)

        site.save()

        return Response({'vazion'}, status=status.HTTP_400_BAD_REQUEST)

class SitesDetail(APIView):

    def get_object(self, pk):
        try:
            return Sites.objects.get(pk=pk)
        except Sites.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        site = self.get_object(pk)
        serializer = SitesSerializer(site)
        return Response(serializer.data)

    def patch(self, request, pk, format=None):
        site = self.get_object(pk)
        serializer = SitesSerializer(site, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        site = self.get_object(pk)
        site.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)