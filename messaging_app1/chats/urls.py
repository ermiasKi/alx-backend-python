from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, UserLogin

router = DefaultRouter()
router.register('conversation', ConversationViewSet, basename='conversation')
router.register('message', MessageViewSet, basename='message')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', UserLogin)
]