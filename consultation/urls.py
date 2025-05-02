from django.urls import path
from .views import ShareDiagnosisView, ChatListView, SendMessageView

urlpatterns = [
    path('share-diagnosis/', ShareDiagnosisView.as_view(), name='share_diagnosis'),
    path('chats/', ChatListView.as_view(), name='chat_list'),
    path('send-message/', SendMessageView.as_view(), name='send_message'),
]
