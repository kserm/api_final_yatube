from rest_framework.pagination import LimitOffsetPagination


class PostsPagination(LimitOffsetPagination):
    limit_query_param = 'limit'
    offset_query_param = 'offset'
