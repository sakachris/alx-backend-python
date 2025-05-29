from rest_framework import serializers
from .models import CustomUser, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model, excluding password and sensitive fields."""

    class Meta:
        model = CustomUser
        fields = [
            "user_id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "profile_picture",
            "phone_number",
            "is_online",
            "last_seen",
        ]


class MessageSerializer(serializers.ModelSerializer):
    """Serializer for the Message model, including sender and conversation details."""

    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["message_id", "sender", "conversation", "message_body", "sent_at"]
        read_only_fields = ["message_id", "sent_at"]


class ConversationSerializer(serializers.ModelSerializer):
    """Serializer for the Conversation model, including participants and messages."""

    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source="messages")

    class Meta:
        model = Conversation
        fields = ["conversation_id", "participants", "created_at", "messages"]
