# chats/permissions.py

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsParticipantOfConversation(BasePermission):
    """
    Allows access only to users who are participants of the conversation or related message.
    Applies to both Conversation and Message objects.
    """

    def has_object_permission(self, request, view, obj):
        # For Conversation objects
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # For Message objects
        if hasattr(obj, "conversation") and hasattr(obj.conversation, "participants"):
            return request.user in obj.conversation.participants.all()

        return False


# # chats/permissions.py
# from rest_framework.permissions import BasePermission
# from .models import Conversation


# class IsConversationParticipant(BasePermission):
#     """
#     Allows access only to users who are participants of the conversation.
#     """

#     def has_object_permission(self, request, view, obj):
#         return request.user in obj.participants.all()


# class IsMessageParticipant(BasePermission):
#     """
#     Allows message access only to users in the associated conversation.
#     """

#     def has_object_permission(self, request, view, obj):
#         return request.user in obj.conversation.participants.all()
