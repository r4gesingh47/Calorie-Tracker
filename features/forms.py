from django import forms
from authentication.models import FoodItem, Goal


class VegForm(forms.Form):
    foods = FoodItem.objects.filter(non_veg=False)
    food_choices = ((food.id, food.name)for food in foods)
    food_choice = forms.ChoiceField(choices=food_choices, required=True)


class NonVegForm(forms.Form):
    foods = FoodItem.objects.all()
    food_choices = ((food.id, food.name)for food in foods)
    food_choice = forms.ChoiceField(choices=food_choices, required=True)


class CalorieForm(forms.Form):
    goals = Goal.objects.all()
    goal_choices = ((goal.id, goal.calorie) for goal in goals)
    goal_choice = forms.ChoiceField(choices=goal_choices, required=True)
