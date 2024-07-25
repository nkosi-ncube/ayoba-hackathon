# CustomerAssistanceAPI/views.py

from django.http import JsonResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def ai_query_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_query = data.get('query', '')
            
            # Here you would send the query to your AI system
            ai_response = send_query_to_ai(user_query)
            
            # Return the AI response
            return JsonResponse({'response': ai_response})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def send_query_to_ai(query):
    # Simulate sending a query to AI and getting a response
    # Replace this with your actual AI interaction logic
    return f"AI response to '{query}'"
