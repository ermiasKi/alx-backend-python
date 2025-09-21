from rest_framework import serializers
from .models import User, Conversation, Message

class UserSerializer(serializers.ModelSerializer):
    # Using serializers.CharField as required
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = ['user_id', 'email', 'first_name', 'last_name', 'full_name', 'phone_number', 'role', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    # Using serializers.SerializerMethodField() as required
    participant_count = serializers.SerializerMethodField()
    
    # Using serializers.CharField as required  
    participants_info = serializers.CharField(source='get_participants_info', read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['conversation_id', 'participants_id', 'created_at', 'participant_count', 'participants_info']
    
    # Required SerializerMethodField implementation
    def get_participant_count(self, obj):
        return obj.participants.count()


class MessageSerializer(serializers.ModelSerializer):
    # Using serializers.CharField as required
    truncated_message = serializers.CharField(source='get_truncated_message', read_only=True)
    
    # Using serializers.SerializerMethodField() as required
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Message
        fields = ['message_id', 'sender_id', 'message_body', 'truncated_message', 'sender_name', 'sent_at']
    
    # Required SerializerMethodField implementation
    def get_sender_name(self, obj):
        return f"{obj.sender.first_name} {obj.sender.last_name}"
    
    # Custom validation using serializers.ValidationError as required
    def validate_message_body(self, value):
        if len(value.strip()) == 0:
            raise serializers.ValidationError("Message body cannot be empty")
        if len(value) > 1000:
            raise serializers.ValidationError("Message is too long (max 1000 characters)")
        return value