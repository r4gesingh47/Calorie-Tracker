from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Goal(models.Model):
    calorie = models.IntegerField()
    plan = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.calorie}'


class FoodItem(models.Model):
    name = models.CharField(max_length=30)
    non_veg = models.BooleanField(default=False, blank=True)
    calorie = models.IntegerField()

    def __str__(self):
        return f"{self.name} - {self.calorie}"


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile', null=True)
    avatar = models.ImageField(
        default='avatars/default.jpg', upload_to='avatars', blank=True)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    height = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    bmi = models.DecimalField(
        max_digits=5, decimal_places=2, blank=True, null=True)
    non_veg = models.BooleanField(default=False)
    calorie_goal = models.ForeignKey(
        Goal, on_delete=models.SET_NULL, null=True, blank=True)

    def get_total_calorie(self):
        foods = self.consumed.all()
        total = 0
        for food in foods:
            total += food.food_id.calorie
        return total

    def __str__(self):
        return f'{self.user.username}'


class Consumed(models.Model):
    food_id = models.ForeignKey(FoodItem, on_delete=models.CASCADE)
    consumed_by = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='consumed')

    def get_name(self):
        return self.food_id.name

    def get_calorie(self):
        return self.food_id.calorie

    def __str__(self):
        return f"{self.food_id.name} -{self.consumed_by.user.username}"
