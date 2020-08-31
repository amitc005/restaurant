from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from .models import Restaurant, FavoriteRestaurant, BlackListedRestaurant
from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework as filters

from .serializer import (
    RestaurantSerializer,
    UserSerializer,
    FavoriteRestaurantSerializer,
    BlackListedRestaurantSerializer,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "restaurants": reverse("restaurant-list", request=request, format=format),
        }
    )


class RestaurantFilter(filters.FilterSet):
    distance_gt = filters.NumberFilter(field_name="office_distance", lookup_expr="gt")
    distance_lt = filters.NumberFilter(field_name="office_distance", lookup_expr="lt")
    open = filters.ChoiceFilter(
        field_name="is_open", choices=(("Y", "YES"), ("N", "NO"))
    )
    postal_code = filters.CharFilter(field_name="postal_code", lookup_expr="contains")
    city = filters.CharFilter(field_name="city", lookup_expr="contains")
    country = filters.CharFilter(field_name="country", lookup_expr="contains")

    class Meta:
        model = Restaurant
        fields = ["open", "distance_lt", "distance_gt"]


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RestaurantFilter

    def get_queryset(self):
        return Restaurant.objects.filter()


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class FavoriteRestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = FavoriteRestaurantSerializer

    def get_queryset(self):
        user_pk = self.kwargs["user_pk"]
        return FavoriteRestaurant.objects.filter(user=user_pk)

    def perform_create(self, serializer):
        user = get_object_or_404(get_user_model(), id=self.kwargs["user_pk"])
        restaurant = get_object_or_404(Restaurant, id=self.request.data["restaurant"])
        is_restaurant_blacklisted = BlackListedRestaurant.objects.filter(
            user=user.id, restaurant=restaurant.id
        )
        if is_restaurant_blacklisted:
            error_msg = (
                f"Restaurant {is_restaurant_blacklisted.__str__()}"
                f"is black listed by the user"
            )
            raise ValidationError({"error_msg": error_msg})
        serializer.save(user=user, restaurant=restaurant)


class BlackListViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BlackListedRestaurantSerializer

    def get_queryset(self):
        user_pk = self.kwargs["user_pk"]
        return BlackListedRestaurant.objects.filter(user=user_pk)

    def perform_create(self, serializer):
        user = get_object_or_404(get_user_model(), id=self.kwargs["user_pk"])
        restaurant = get_object_or_404(Restaurant, id=self.request.data["restaurant"])
        favorite_restaurant = FavoriteRestaurant.objects.get(
            user=user.id, restaurant=restaurant.id
        )
        if favorite_restaurant:
            favorite_restaurant.delete()
        serializer.save(user=user, restaurant=restaurant)
