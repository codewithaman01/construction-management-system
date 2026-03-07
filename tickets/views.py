# ✅ FIXED — tickets/views.py
import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import Ticket


@login_required
def ticket_page(request):
    return render(request, 'tickets/create_ticket.html')


@login_required
def track_tickets_page(request):            # ✅ NEW — was completely missing
    return render(request, 'tickets/track_tickets.html')


@login_required
def get_tickets(request):                   # ✅ NEW — was completely missing
    tickets = Ticket.objects.filter(created_by=request.user).order_by('-created_at')
    data = [{
        'id':          t.id,
        'title':       t.title,
        'description': t.description,
        'status':      t.status,
        'latitude':    t.latitude,
        'longitude':   t.longitude,
        'created_at':  t.created_at.strftime('%Y-%m-%d %H:%M'),
    } for t in tickets]
    return JsonResponse({'tickets': data})


@login_required
@csrf_exempt
@require_POST
def save_ticket(request):
    data = json.loads(request.body)

    if not data.get('title') or not data.get('description'):
        return JsonResponse({'error': 'Title and description are required'}, status=400)

    Ticket.objects.create(
        title       = data['title'],
        description = data['description'],
        image_data  = data.get('image', ''),
        latitude    = data.get('latitude'),    # ✅ GPS saved
        longitude   = data.get('longitude'),   # ✅ GPS saved
        created_by  = request.user,
    )
    return JsonResponse({'status': 'success'})


@login_required
@csrf_exempt
@require_POST
def update_ticket_status(request):          # ✅ NEW — for tracking page
    data      = json.loads(request.body)
    ticket    = get_object_or_404(Ticket, id=data.get('id'))
    ticket.status = data.get('status')
    ticket.save()
    return JsonResponse({'status': 'updated'})