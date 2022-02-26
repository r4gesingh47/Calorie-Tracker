from django.contrib import admin
from .models import Profile, Consumed, Goal, FoodItem
# Register your models here.


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'weight', 'height', 'bmi', 'calorie_goal')


admin.site.register(Consumed)
admin.site.register(Goal)
admin.site.register(FoodItem)
