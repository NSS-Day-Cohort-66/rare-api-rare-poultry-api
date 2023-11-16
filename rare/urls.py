from django.contrib import admin
from rest_framework.routers import DefaultRouter
from django.conf.urls import include
from django.urls import path
from rareapi.views import register_user, login_user, CategoryView

router = DefaultRouter(trailing_slash=False)
router.register(r'categories', CategoryView, 'categories')

urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
