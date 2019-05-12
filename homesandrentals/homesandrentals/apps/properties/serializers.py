import re
import json
from rest_framework import serializers
from .models import Property
from django.forms import URLField
from datetime import datetime
from django.utils.timezone import get_current_timezone
from django.template.defaultfilters import slugify


class AddPropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('title', 'slug', 'username', 'price', 'currency', 'type',
                  'available', 'description', 'location', 'coordinates', 'media')
        read_only_fields = ('slug', )

    def validate_media(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError(
                'please provide media for this item.')

        url = URLField()
        for item in value:
            if not url.clean(item):
                raise serializers.ValidationError('please provide valid urls.')

        return value

    def get_slug(self, title):
        return slugify(f'{title}{datetime.now().isoformat()}')


class UpdatePropertySerializer(serializers.ModelSerializer):

    class Meta:
        model = Property
        fields = ('title', 'price', 'currency', 'type', 'available',
                  'description', 'location', 'coordinates', 'media')

    def validate_media(self, value):
        if len(value) <= 0:
            raise serializers.ValidationError(
                'please provide media for this item.')

        url = URLField()
        for item in value:
            if not url.clean(item):
                raise serializers.ValidationError('please provide valid urls.')

        return value

    def update(self, instance, validated_data):
        instance.title = validated_data['title']
        instance.price = validated_data['price']
        instance.currency = validated_data['currency']
        instance.type = validated_data['type']
        instance.available = validated_data['available']
        instance.description = validated_data['description']
        instance.location = validated_data['location']
        instance.coordinates = validated_data['coordinates']
        instance.media = validated_data['media']
        instance.updated_at = datetime.now(
            tz=get_current_timezone()).isoformat()
        instance.save()
        return instance


class GetPropertySerializer(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ('title', 'price', 'currency', 'type', 'available',
                  'description', 'location', 'coordinates', 'media')
