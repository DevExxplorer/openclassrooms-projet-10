from rest_framework import routers
from django.contrib import admin
from django.urls import include, path
from api import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.SimpleRouter()
router.register('users', views.UserViewSet, basename='user')
router.register('projects', views.ProjectViewSet, basename='projects')
router.register('issues', views.IssueViewSet, basename='issues')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
