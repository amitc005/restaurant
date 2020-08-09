from rest_framework import serializers

from django.contrib.auth import get_user_model

from .models import Restaurant, FavoriteRestaurant, BlackListedRestaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    urls = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "urls")

    def get_urls(self, obj):
        return {
            "favorite_restaurants": self.context["request"].build_absolute_uri(
                f"/api/users/{obj.id}/favorite_restaurants/"
            ),
            "blacklist_restaurants": self.context["request"].build_absolute_uri(
                f"/api/users/{obj.id}/blacklist_restaurants/"
            ),
        }


class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    restaurants = serializers.SerializerMethodField()

    class Meta:
        model = FavoriteRestaurant
        fields = ("restaurants", "id")

    def get_restaurants(self, obj):
        serialize = RestaurantSerializer(obj.restaurant)
        return serialize.data


class BlackListedRestaurantSerializer(serializers.ModelSerializer):
    restaurants = serializers.SerializerMethodField()

    class Meta:
        model = BlackListedRestaurant
        fields = ("restaurants",)

    def get_restaurants(self, obj):
        serialize = RestaurantSerializer(obj.restaurant)
        return serialize.data
