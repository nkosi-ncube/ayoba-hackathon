# CustomerAssistanceAPI/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('queries/', views.ai_query_response, name='ai_query_response'),
]

