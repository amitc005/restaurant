from rest_framework.routers import SimpleRouter
from .views import RestaurantViewSet, UserViewSet

router = SimpleRouter()
router.register("restaurants", RestaurantViewSet, basename="restaurants")
router.register("users", UserViewSet, basename="users")
urlpatterns = router.urls
