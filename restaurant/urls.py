from rest_framework_nested import routers
from django.urls import path
from .views import (
    RestaurantViewSet,
    UserViewSet,
    FavoriteRestaurantViewSet,
    BlackListViewSet,
    api_root,
)

router = routers.SimpleRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurant")
router.register("users", UserViewSet, basename="user")
users_router = routers.NestedSimpleRouter(router, r"users", lookup="user")
users_router.register(
    r"favorite_restaurants", FavoriteRestaurantViewSet, basename="favorite_restaurant"
)
users_router.register(
    r"blacklist_restaurants", BlackListViewSet, basename="blacklist_restaurant"
)
urlpatterns = [*router.urls, *users_router.urls, path("", api_root)]
