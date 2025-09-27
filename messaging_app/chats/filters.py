import django_filters
from .models import Message, Conversation


class MessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="gte")
    end_date = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr="lte")

    # Filter by sender (user id)
    sender = django_filters.UUIDFilter(field_name="sender__user_id")

    # Filter by conversation (conversation id)
    conversation = django_filters.UUIDFilter(field_name="Conversation__Conversation_id")

    class Meta:
        model = Message
        fields = ["sender", "conversation", "start_date", "end_date"]