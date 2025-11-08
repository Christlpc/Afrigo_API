from django.urls import path
from django.http import JsonResponse
import time

def health_check(request):
    return JsonResponse({
        'status': 'OK',
        'timestamp': time.time(),
        'uptime': time.time()  # Simplifié, utiliser psutil en production
    })

urlpatterns = [
    path('', health_check, name='health'),
]

