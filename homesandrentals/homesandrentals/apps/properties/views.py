from django.shortcuts import render
from rest_framework.generics import CreateAPIView, UpdateAPIView, DestroyAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework import exceptions
from .serializers import (AddPropertySerializer,
                          UpdatePropertySerializer, GetPropertySerializer)
from .renderers import PropertyRenderer, PropertyListRenderer
from .models import Property
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
import datetime


class AddPropertyView(CreateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (PropertyRenderer,)
    serializer_class = AddPropertySerializer

    def post(self, request):
        request_data = request.data.get('property', {})
        serializer = self.serializer_class(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save(slug=serializer.get_slug(request_data.get('title')))
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateProperty(UpdateAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (PropertyRenderer,)
    serializer_class = UpdatePropertySerializer
    look_url_kwarg = 'id'

    def get_queryset(self):
        id = self.kwargs.get(self.look_url_kwarg)
        return Property.objects.filter(id=id)

    def put(self, request, *args, **kwargs):
        request_data = request.data.get('property', {})
        queryset = self.get_queryset()

        if not queryset:
            raise exceptions.APIException('Item not found.')
        else:
            updated_property = self.serializer_class().update(
                queryset[0], request_data)
            return Response(data=self.serializer_class(updated_property).data, status=status.HTTP_201_CREATED)


class DeletePropertyView(DestroyAPIView):
    permission_classes = (AllowAny,)
    look_url_kwarg = 'id'

    def delete(self, request, *args, **kwargs):
        id = self.kwargs.get(self.look_url_kwarg)
        property = Property.objects.filter(id=id)
        if property:
            property.delete()
            return Response({'message': 'Property was deleted.'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'No such property was found.'}, status=status.HTTP_404_NOT_FOUND)


class GetAllPropertyView(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetPropertySerializer
    pagination_class = PageNumberPagination
    renderer_classes = (PropertyListRenderer,)

    def get_queryset(self):
        property_list = Property.objects.all().order_by('id')
        if property_list is not None:
            return property_list


class GetPropertyById(APIView):
    permission_classes = (AllowAny,)
    serializer_class = GetPropertySerializer
    renderer_classes = (PropertyListRenderer,)
    look_url_kwarg = 'id'

    def get(self, *args, **kwargs):
        id = self.kwargs.get(self.look_url_kwarg)
        property = Property.objects.filter(id=id)
        serializer = self.serializer_class(property, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetPropertyByLocation(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetPropertySerializer
    renderer_classes = (PropertyListRenderer,)
    look_url_kwarg = 'location'

    def get_queryset(self):
        location = self.kwargs.get(self.look_url_kwarg)
        property_list = Property.objects.filter(
            location__icontains=location).order_by('id')
        if property_list is not None:
            return property_list


class GetPropertyByTitle(ListAPIView):
    permission_classes = (AllowAny,)
    serializer_class = GetPropertySerializer
    renderer_classes = (PropertyListRenderer,)
    look_url_kwarg = 'title'

    def get_queryset(self):
        title = self.kwargs.get(self.look_url_kwarg)
        property_list = Property.objects.filter(
            title__icontains=title).order_by('id')
        if property_list is not None:
            return property_list
