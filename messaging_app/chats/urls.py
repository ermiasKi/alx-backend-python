from django.urls import path, include
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet
from rest_framework import routers


router = NestedDefaultRouter()
router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename="conversations")
router.register(r'messages', MessageViewSet, basename="messages")

urlpatterns = [
    path('', include(router.urls)),
]