from django.db import models

class SiteCategory(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f'{self.description}'

class SiteURL(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(null=False, max_length=100)

    def __str__(self):
        return f'{self.description}'

class Sites(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(null=False, max_length=100, unique=True)
    active = models.BooleanField(default=True)
    url = models.ManyToManyField(SiteURL, related_name='url')
    category = models.ManyToManyField(SiteCategory, related_name='category')