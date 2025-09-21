from rest_framework import serializers
from .models import user, conversation, message

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user()
        fields = ['email', 'last_name', 'first_name', 'created_at', 'role', 'phone_number', 'user_id']


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = conversation()
        fields = ['created_at', 'participants_id', 'conversation_id']


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = message()
        fields = ['sent_at', 'message_body', 'sender_id', 'message_id']