from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import LoginView, RegisterView, logout_request, profile, UpdateProfileView

urlpatterns = [
    path('login_user', LoginView.as_view(), name='login_user'),
    path('register', RegisterView.as_view(), name='register'),
    path('logout', logout_request, name='logout'),
    path('profile', profile, name='profile'),
    path('update', UpdateProfileView.as_view(), name='update')
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
