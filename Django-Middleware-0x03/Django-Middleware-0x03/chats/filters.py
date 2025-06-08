# chats/filters.py

import django_filters
from .models import Message


class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="timestamp", lookup_expr="lte")
    sender = django_filters.CharFilter(field_name="sender__user_id", lookup_expr="exact")
    conversation = django_filters.CharFilter(field_name="conversation__conversation_id", lookup_expr="exact")

    class Meta:
        model = Message
        fields = ['start_date', 'end_date', 'sender', 'conversation']
