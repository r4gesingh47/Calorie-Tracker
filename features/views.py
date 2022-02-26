from django.shortcuts import render, reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.views import View
from django.contrib import messages
from .forms import VegForm, NonVegForm, CalorieForm
import json
import threading
from authentication.models import Consumed, FoodItem, Goal
import time
# Create your views here.


@login_required
def calorie_intake(request):
    u = request.user
    consumed_list = u.profile.consumed
    if request.method == 'POST':
        if u.profile.non_veg:
            form = NonVegForm(request.POST)
        else:
            form = VegForm(request.POST)
        if form.is_valid():
            food_id = form.cleaned_data['food_choice']
            food_obj = FoodItem.objects.get(id=food_id)
            Consumed.objects.create(food_id=food_obj, consumed_by=u.profile)
            messages.success(request, f'you consumed {food_obj.name}')
        else:
            messages.error(request, 'Invalid')
    else:
        if u.profile.non_veg:
            form = NonVegForm()
        else:
            form = VegForm()
    return render(request, 'features/calorie_intake.html', {
        'form': form,
        'title': 'Intake',
        'consumed': consumed_list.all(),
    })


@login_required
def remove(request, id):
    c = Consumed.objects.get(id=id)
    if c:
        c.delete()
    return HttpResponseRedirect(reverse('features:intake'))


@login_required
def calorie_goals(request):
    p = request.user.profile
    table = None
    if p.calorie_goal:
        plan_path = p.calorie_goal.plan
        with open(plan_path, 'r') as f:
            table = json.loads(f.read())
        if p.non_veg:
            table = table[0]['non_veg']
        else:
            table = table[0]['veg']
    if request.method == "POST":
        form = CalorieForm(request.POST)
        if form.is_valid():
            goal_obj = Goal.objects.get(id=form.cleaned_data['goal_choice'])
            p.calorie_goal = goal_obj
            p.save()
            messages.success(
                request, f'Your update goal is now {goal_obj.calorie}')
            return HttpResponseRedirect(reverse('features:goals'))
    else:
        form = CalorieForm()
    return render(request, 'features/calorie_goals.html', {
        'form': form,
        'title': 'Goal',
        'table': table
    })
