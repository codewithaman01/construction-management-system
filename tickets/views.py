import json
from django.http import JsonResponse
from django.shortcuts import render
from .models import Ticket


def ticket_page(request):
    return render(request, 'tickets/create_ticket.html')


def save_ticket(request):
    data = json.loads(request.body)

    Ticket.objects.create(
        title=data['title'],
        description=data['description'],
        image_data=data['image'],  # stored in DB
        created_by=request.user
    )

    return JsonResponse({'status': 'success'})