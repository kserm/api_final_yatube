from rest_framework import routers

from django.urls import include, path

from api import views


router = routers.DefaultRouter()
router.register(r'api/v1/posts', views.PostViewSet)
router.register(r'api/v1/groups', views.GroupViewSet)
router.register(r'api/v1/posts/(?P<post_id>\d+)/comments',
                views.CommentViewSet,
                basename='comments')
router.register(r'api/v1/follow', views.FollowViewSet,
                basename='follow')

urlpatterns = [
    path('', include(router.urls)),
]
