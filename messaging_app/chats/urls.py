from django.urls import path, include
from rest_framework import routers
from .views import ConversationViewSet, MessageViewSet


router = routers.DefaultRouter()
router.register('conversations', ConversationViewSet, basename="conversations")

router.register('messages', MessageViewSet, basename="messages")


urlpatters = [
    path('', include(router.urls)),
]