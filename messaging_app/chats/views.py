from django.shortcuts import render
from rest_framework import viewsets
from .models import conversation, message
from .serializers import ConversationSerializer, MessageSerializer

# Create your views here.

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = conversation.objects.all()
    serializer_class = ConversationSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = message.objects.all()
    serializer_class = MessageSerializer
