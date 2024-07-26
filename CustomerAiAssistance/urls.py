# CustomerAssistanceAPI/urls.py

# CustomerAiAssistance/urls.py
from django.urls import path
from .views import QueryAPIView

urlpatterns = [
    path('queries/', QueryAPIView.as_view(), name='query-api'),
]
