from django.shortcuts import get_object_or_404

from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from posts.models import Post, Group, Comment, Follow
from .serializers import PostSerializer, CommentSerializer, GroupSerializer
from .serializers import FollowSerializer
from .user_permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    '''Создает пост или возвращает список постов'''
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        '''Получение объекта - автор поста'''
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    '''Создает комментaрий или возвращает список комментариев'''
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrReadOnly, IsAuthenticated)

    def get_queryset(self):
        '''Возвращает список комментариев'''
        post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
        queryset = post.comments.all()
        return queryset

    def perform_create(self, serializer):
        '''Проверка наличия поста для комментариев'''
        post_id = self.kwargs.get('post_id')
        get_object_or_404(Post, id=post_id)
        serializer.save(author=self.request.user, post_id=post_id)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    '''Получает группу или список групп'''
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class FollowViewSet(viewsets.ModelViewSet):
    '''Получает группу или список групп'''
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user',)
    permission_classes = (IsAuthenticated,)
