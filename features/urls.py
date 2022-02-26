from django.urls import path
from .views import calorie_intake, calorie_goals, remove
urlpatterns = [
    path('intake', calorie_intake, name='intake'),
    path('goals', calorie_goals, name='goals'),
    path('remove/<int:id>', remove, name='remove')
]
