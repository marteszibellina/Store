"""PAGINATION for API"""

from rest_framework.pagination import PageNumberPagination

from store.settings import PAGE_SIZE


class StandartPagination(PageNumberPagination):
    """Pagination for API viewsets"""

    page_size = PAGE_SIZE
    page_size_query_param = 'limit'
