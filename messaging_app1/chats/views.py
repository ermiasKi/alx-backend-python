from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action, api_view
from .models import Conversation, Message, User
from .serializers import UserSerializer, ConversationSerializer, MessageSerializer
from .auth import user_authenticate
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt

@api_view(['post'])
def UserLogin(request):

    # data = UserSerializer(request.data)
    user = user_authenticate(request.data)

    token, created = Token.objects.get_or_create(user=user)

    data = UserSerializer(user).data

    return Response({
        'token': token.key,
        'user': data
    }, status=status.HTTP_200_OK)



class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    @action(detail=False, methods=['post'])
    def new_conversation(self, request):
        participants = request.data.get('participants',[])

        if not participants or len(participants) < 2:
            return Response({"error":"2 participants is must"},
                status=status.HTTP_400_BAD_REQUEST
                )
        
        conversation = Conversation.objects.create()
        conversation.participants.set(User.objects.filter(id__in=participants))
        conversation.save()

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


    @action(detail=False, methods=['post'])
    def send_message(self, request, pk=None):

        conversation = Conversation.objects.filter(pk=pk).first()
        if not conversation:
            return Response({"error":"conversation not found"}, status=status.HTTP_404_NOT_FOUND)
        
        sender_id = request.data.get("sender")
        message_body = request.data.get("message_body")

        if not sender_id or not message_body:
            return Response(
                {"error":"Both sender and messsage_body are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        sender = User.objects.filter(pk=sender_id).first()
        if not sender:
            return Response({"error":"sender not found"}, status=status.HTTP_404_NOT_FOUND)
        
        message = Message.objects.create(
            sender = sender,
            conversation = conversation,
            message_body = message_body
        )

        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
