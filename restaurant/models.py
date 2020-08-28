from django.db import models

from django.contrib.auth.models import User


class Restaurant(models.Model):

    #  Please make use boolean
    class Open(models.TextChoices):
        YES = "Y"
        NO = "N"

    name = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    postal_code = models.CharField(max_length=15)
    street = models.CharField(max_length=30)
    office_distance = models.IntegerField(default=0)
    is_open = models.CharField(choices=Open.choices, max_length=1, default=Open.YES)

    def __str__(self):
        return self.name


class FavoriteRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="favorite_restaurant", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "restaurant"),)

    def __str__(self):
        return self.restaurant.name


class BlackListedRestaurant(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    user = models.ForeignKey(
        User, related_name="black_list_restaurants", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("user", "restaurant"),)

    def __str__(self):
        return self.restaurant.name
