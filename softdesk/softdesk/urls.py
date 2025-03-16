from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from api import views

router = routers.SimpleRouter()
router.register('users', views.UserViewSet, basename='user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
