from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ShareDiagnosisView, 
    ChatListView, 
    SendMessageView,
    ChatSessionViewSet,
    ChatMessageViewSet
)

router = DefaultRouter()
router.register(r'chat-sessions', ChatSessionViewSet, basename='chat-session')

chat_message_router = DefaultRouter()
chat_message_router.register(r'messages', ChatMessageViewSet, basename='chat-message')

urlpatterns = [
    path('share-diagnosis/', ShareDiagnosisView.as_view(), name='share_diagnosis'),
    path('chats/', ChatListView.as_view(), name='chat_list'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
    path('', include(router.urls)),
    path('chat-sessions/<int:session_pk>/', include(chat_message_router.urls)),
]
