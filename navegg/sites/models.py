from django.db import models

# Create your models here.
class Sites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100)
    active = models.BooleanField(default=True)
    url = models.CharField(null=False, max_length=100)
    category = models.CharField(null=False, max_length=100)