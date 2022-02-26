from django.shortcuts import render, reverse
from django.views import View
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from io import BytesIO
from django.core.files import File
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import LoginForm, RegisterForm, UpdateProfileForm
from .models import Profile
# Create your views here.


class LoginView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        form = LoginForm()
        return render(request, 'authentication/login.html', {
            'form': form,
            'title': 'Login'
        })

    def post(self, request):
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Your are now logged in as {username}')
                print('login successfull')
                return HttpResponseRedirect(reverse('home'))
        else:
            messages.warning(request, 'Invalid Credentials')

        return render(request, 'authentication/login.html', {
            'form': form,
            'title': 'Login'
        })


class RegisterView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('home'))
        form = RegisterForm()
        return render(request, 'authentication/register.html', {
            'form': form,
            'title': 'Register'
        })

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            u1 = form.save()
            Profile.objects.create(user=u1)
            messages.success(request, "User created!!")
            return HttpResponseRedirect(reverse('authentication:login_user'))
        else:
            messages.warning(request, 'Invalid Data')

        return render(request, 'authentication/register.html', {
            'form': form,
            'title': 'Register'
        })

@login_required
def profile(request):
    return render(request, 'authentication/profile.html', {
        'title': 'Profile'
    })


class UpdateProfileView(View):
    def get(self, request):
        p = Profile.objects.get(user=request.user)
        form = UpdateProfileForm(instance=p)
        return render(request, 'authentication/update_profile.html', {
            'form': form,
            'title': 'Update'
        })

    def post(self, request):
        p = Profile.objects.get(user=request.user)

        files = request.FILES
        img = files.get('avatar')
        if img:
            i = Image.open(img)
            i = i.convert('RGB')
            thumb_io = BytesIO()
            i.save(thumb_io, format='JPEG', qualtiy=80)
            inmemory = InMemoryUploadedFile(
                thumb_io, None, f'{p.user.username}.jpeg', 'image/jpeg', thumb_io.tell(), None)
        form = UpdateProfileForm(request.POST, instance=p)
        if form.is_valid():
            updated_p = form.save()
            if img:
                updated_p.avatar = inmemory
                updated_p.save()
            messages.success(request, "Updated successfully")
            return HttpResponseRedirect(reverse('authentication:profile'))
        else:
            messages.error(request, 'Invalid Data')
        return render(request, 'authentication/update_profile.html', {
            'form': form,
            'title': 'Update'
        })


@login_required
def logout_request(request):
    logout(request)
    messages.info(request,'Bye Bye see you soon')
    return HttpResponseRedirect(reverse('home'))
