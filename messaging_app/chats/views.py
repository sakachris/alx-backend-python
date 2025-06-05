# chats/views.py

from rest_framework import viewsets, filters
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django_filters.rest_framework import DjangoFilterBackend
from .models import Message, Conversation, CustomUser
from .serializers import MessageSerializer, ConversationSerializer
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from django.shortcuts import get_object_or_404


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["created_at"]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        participant_ids = self.request.data.get("participants", [])
        if not participant_ids:
            raise PermissionDenied("Participants are required.")

        participants = CustomUser.objects.filter(user_id__in=participant_ids)
        if not participants.exists():
            raise PermissionDenied("No valid participants found.")

        conversation = serializer.save()
        conversation.participants.add(self.request.user, *participants)
        conversation.save()


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ["message_body"]
    filterset_class = MessageFilter

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        conversation = serializer.validated_data["conversation"]
        if self.request.user not in conversation.participants.all():
            raise PermissionDenied("You are not part of this conversation.")
        serializer.save(sender=self.request.user)


# # chats/views.py
# from rest_framework import viewsets, status, filters
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.exceptions import PermissionDenied
# from .models import Conversation, Message, CustomUser
# from .serializers import ConversationSerializer, MessageSerializer
# from .permissions import IsConversationParticipant, IsMessageParticipant
# from django.shortcuts import get_object_or_404


# class ConversationViewSet(viewsets.ModelViewSet):
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated, IsConversationParticipant]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ["created_at"]

#     def get_queryset(self):
#         """Return conversations for the authenticated user only."""
#         return Conversation.objects.filter(participants=self.request.user)

#     def perform_create(self, serializer):
#         """Create a new conversation and add authenticated user as a participant."""
#         participant_ids = self.request.data.get("participants", [])
#         if not participant_ids:
#             raise PermissionDenied("Participants are required.")

#         participants = CustomUser.objects.filter(user_id__in=participant_ids)
#         if not participants.exists():
#             raise PermissionDenied("No valid participants found.")

#         conversation = serializer.save()
#         conversation.participants.add(self.request.user, *participants)
#         conversation.save()


# class MessageViewSet(viewsets.ModelViewSet):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated, IsMessageParticipant]
#     filter_backends = [filters.SearchFilter]
#     search_fields = ["message_body"]

#     def get_queryset(self):
#         """Return messages for the authenticated user's conversations."""
#         return Message.objects.filter(conversation__participants=self.request.user)

#     def perform_create(self, serializer):
#         conversation = serializer.validated_data["conversation"]
#         if self.request.user not in conversation.participants.all():
#             raise PermissionDenied("You are not part of this conversation.")

#         serializer.save(sender=self.request.user)
