# chats/permissions.py

from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation or a related message
    to view, edit, or delete the object.
    """

    def has_object_permission(self, request, view, obj):
        # If the object is a Conversation, check if the user is a participant
        if hasattr(obj, "participants"):
            return request.user in obj.participants.all()

        # If the object is a Message, check if the user is a participant of its conversation
        if hasattr(obj, "conversation") and hasattr(obj.conversation, "participants"):
            return request.user in obj.conversation.participants.all()

        # Deny access by default
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
