from django.db import models
from django.template.defaultfilters import slugify
from ..users.models import User
from django.contrib.postgres import fields
from datetime import datetime


class Property(models.Model):
    title = models.CharField(max_length=255)
    username = models.ForeignKey(
        User, max_length=255, on_delete=models.CASCADE, related_name='property')
    price = models.IntegerField(default=0)
    currency = models.CharField(max_length=10)
    type = models.CharField(max_length=255)
    available = models.BooleanField(default=False)
    description = models.TextField()
    location = models.CharField(max_length=255)
    coordinates = models.CharField(max_length=100)
    slug = models.SlugField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)
    media = fields.ArrayField(models.CharField(max_length=100), blank=True, default=list)

