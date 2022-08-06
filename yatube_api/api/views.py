from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from posts.models import Post, Group, Follow

from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .serializers import FollowSerializer
from .permission import IsAuthor
from .pagination import PostsPagination


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthor]
    pagination_class = PostsPagination

    def check_permissions(self, request):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        return super().check_permissions(request)

    def check_object_permissions(self, request, obj):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        return super().check_object_permissions(request, obj)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        post = Post.objects.get(
            pk=self.kwargs.get("post_id")
        )
        new_queryset = post.comments
        return new_queryset

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        post = Post.objects.get(pk=post_id)
        serializer.save(author=self.request.user,
                        post=post)

    def check_object_permissions(self, request, obj):
        if not request.user.is_authenticated:
            return Response(status=status.HTTP_200_OK)
        return super().check_object_permissions(request, obj)


class FollowViewSet(viewsets.ModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['following__username']

    def get_queryset(self):
        user = self.request.user
        new_queryset = Follow.objects.filter(user=user)
        return new_queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
