from django.contrib import admin
from django.urls import include, path
from rest_framework_nested import routers

from api.views import UserViewSet, ProjectViewSet, IssueViewSet, ContributorViewSet, CommentViewSet

router = routers.SimpleRouter()

router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='projects')

projects_router = routers.NestedSimpleRouter(router, r'projects', lookup='project')
projects_router.register(r'issues', IssueViewSet, basename='project-issues')
projects_router.register('contributors', ContributorViewSet, basename='project-contributors')

issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
issues_router.register(r'comments', CommentViewSet, basename='issue-comments')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include(projects_router.urls)),

path('api/', include(issues_router.urls)),
]




#issues_router = routers.NestedSimpleRouter(projects_router, r'issues', lookup='issue')
#issues_router.register('comments', CommentViewSet, basename='issue-comments')

#from rest_framework_simplejwt.views import (
#    TokenObtainPairView,
#   TokenRefreshView,
# )

# path('api/', include(projects_router.urls)),
# path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
# path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),