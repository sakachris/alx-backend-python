from rest_framework.permissions import BasePermission
from .models import Conversation

class IsConversationParticipant(BasePermission):
    """
    Allows access only to users who are participants of the conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.participants.all()


class IsMessageParticipant(BasePermission):
    """
    Allows message access only to users in the associated conversation.
    """

    def has_object_permission(self, request, view, obj):
        return request.user in obj.conversation.participants.all()
