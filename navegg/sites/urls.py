from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from sites import views

app_name = 'sites'
urlpatterns = [
    path('', views.SitesList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)