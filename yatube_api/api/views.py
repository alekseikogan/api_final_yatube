from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework import filters
from rest_framework import permissions
from rest_framework import mixins
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Post, Group, Comment
from .serializers import PostSerializer, CommentSerializer, GroupSerializer
from .serializers import FollowSerializer
from .user_permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Создает пост или возвращает список постов"""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        """Получение объекта - автор поста"""
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    """Создает комментaрий или возвращает список комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly,)

    def get_queryset(self):
        """Возвращает список комментариев"""
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        """Проверка наличия поста для комментариев"""
        post_id = self.kwargs.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Получает группу или список групп"""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class FollowViewSet(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """Возращает подписки пользователя или офрмляет подписку"""
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('following__username',)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Получает список подписок пользователя"""
        user = self.request.user
        return user.follower.all()

    def perform_create(self, serializer):
        """Оформляет подписку на автора"""
        user = self.request.user
        serializer.save(user=user)
