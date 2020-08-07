from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Restaurant, FavoriteRestaurant, BlackListedRestaurant


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    favorite_restaurants = serializers.StringRelatedField(many=True)
    black_list_restaurants = serializers.StringRelatedField(many=True)

    class Meta:
        model = get_user_model()
        fields = ("id", "username", "favorite_restaurants", "black_list_restaurants")


class FavoriteRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRestaurant
        fields = "__all__"

    def create(self, validated_data):
        black_rest = BlackListedRestaurant.objects.filter(
            user=validated_data["user"], restaurant=validated_data["restaurant"]
        )
        if black_rest:
            raise serializers.ValidationError("Can not add blacklisted restaurants")
        return FavoriteRestaurant.objects.create(**validated_data)


class BlackListedRestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlackListedRestaurant
        fields = "__all__"

    def create(self, validated_data):
        fav_rest = FavoriteRestaurant.objects.filter(
            user=validated_data["user"], restaurant=validated_data["restaurant"]
        )
        if fav_rest:
            raise fav_rest.delete()
        return BlackListedRestaurant.objects.create(**validated_data)
