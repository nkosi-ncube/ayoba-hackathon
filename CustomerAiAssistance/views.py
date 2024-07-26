# CustomerAssistanceAPI/views.py
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import QuerySerializer
from .utils import generate_normal_response
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
class QueryAPIView(APIView):
    def post(self, request):
        serializer = QuerySerializer(data=request.data)
        if serializer.is_valid():
            query = serializer.validated_data['query']
            # Call the generate_normal_response function to get the AI's response
            ai_response = generate_normal_response(query)
            response_data = {
                "response": ai_response
            }
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


