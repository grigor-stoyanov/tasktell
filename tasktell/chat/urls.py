from django.urls import path
from tasktell.chat.views import ChatDetailsView

urlpatterns = [
    path('<int:pk>/<int:id>/', ChatDetailsView.as_view(), name='chat')
]
