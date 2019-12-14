from django.shortcuts import render
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