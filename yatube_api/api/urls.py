from django.urls import path, include
from rest_framework import routers

from api.views import PostViewSet, GroupViewSet, CommentViewSet, FollowViewSet


router = routers.DefaultRouter('v1')
router.register(r'posts', PostViewSet, basename='posts')
router.register(r'groups', GroupViewSet, basename='groups')
router.register(
    r'posts/(?P<post_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)
router.register(r'follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
]
