from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rareapi.views import register_user, login_user

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]