### chats/pagination.py

from rest_framework.pagination import PageNumberPagination

class MessagePagination(PageNumberPagination):
    """
    Paginates message list to return 20 messages per page.
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
