from django.shortcuts import render
from django.http import Http404
from sites.models import Sites
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
        serializer = SitesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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