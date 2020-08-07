from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Restaurant, FavoriteRestaurant, BlackListedRestaurant
from .serializer import (
    RestaurantSerializer,
    UserSerializer,
    FavoriteRestaurantSerializer,
    BlackListedRestaurantSerializer,
)

# Create your views here.


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def favorite_restaurants(self, request, pk=None):
        favor_list = FavoriteRestaurant.objects.filter(user=pk)
        serial_data = FavoriteRestaurantSerializer(favor_list, many=True)
        return Response(serial_data.data)

    @favorite_restaurants.mapping.post
    def post_favorite_restaurants(self, request, pk=None):
        serial_post = FavoriteRestaurantSerializer(data=request.data)
        serial_post.is_valid(raise_exception=True)
        serial_post.save()
        return Response(status=201)

    @action(detail=True, methods=["get"])
    def black_list_restaurants(self, request, pk=None):
        black_list = BlackListedRestaurant.objects.filter(user=pk)
        serial_data = BlackListedRestaurantSerializer(black_list, many=True)
        return Response(serial_data.data)

    @black_list_restaurants.mapping.post
    def post_black_list_restaurants(self, request, pk=None):
        serial_post = BlackListedRestaurantSerializer(data=request.data)
        serial_post.is_valid(raise_exception=True)
        serial_post.save()
        return Response(status=201)
