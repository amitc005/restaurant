from rest_framework.routers import SimpleRouter
from django.urls import path
from .views import (
    RestaurantViewSet,
    UserViewSet,
    FavoriteRestaurantAPI,
    FavoriteRestaurantListAPI,
    BlackListRestaurantListAPI,
    api_root,
    BlackListedRestaurantAPI,
)

router = SimpleRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("users", UserViewSet, basename="user")
urlpatterns = [
    *router.urls,
    path(
        "favorite_restaurants/<int:pk>",
        FavoriteRestaurantAPI.as_view(),
        name="favorite-restaurant-detail",
    ),
    path(
        "<users>/<int:user_pk>/favorite_restaurants/",
        FavoriteRestaurantListAPI.as_view(),
        name="favorite-restaurants-list",
    ),
    path(
        "<users>/<int:user_pk>/blacklist_restaurants/",
        BlackListRestaurantListAPI.as_view(),
        name="black-restaurants-list",
    ),
    path(
        "<users>/<int:user_pk>/blacklist_restaurants/<restaurant_pk>/",
        BlackListedRestaurantAPI.as_view(),
        name="black-restaurants-detail",
    ),
    path("", api_root),
]
