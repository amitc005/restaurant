from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.exceptions import ValidationError
from .models import Restaurant, FavoriteRestaurant, BlackListedRestaurant
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


class RestaurantViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer

    def get_queryset(self):
        return Restaurant.objects.filter(**self._get_query_params())

    # Filter
    def _get_query_params(self):
        model_query_map = {
            "distance": "office_distance",
            "distance_gt": "office_distance__gt",
            "distance_lt": "office_distance__lt",
            "open": "is_open",
            "postal_code": "postal_code__icontains",
            "city": "city__icontains",
            "country": "country__icontains",
        }
        return {
            model_query_map[param]: self.request.query_params[param]
            for param in model_query_map.keys()
            if self.request.query_params.get(param)
        }


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
