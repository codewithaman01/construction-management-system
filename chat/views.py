import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import ChatRoom, RoomMember, Message
from accounts.models import User


@login_required
def chat_home(request):
    return render(request, 'chat/chat.html')


# ── helpers — NO .exists() anywhere, fetch IDs into Python then check in-memory

def _room_ids_for_user(user_id):
    return list(RoomMember.objects.filter(user_id=user_id).values_list('room_id', flat=True))

def _user_ids_in_room(room_id):
    return list(RoomMember.objects.filter(room_id=room_id).values_list('user_id', flat=True))

def _is_member(room_id, user_id):
    """Done in Python — avoids djongo's broken EXISTS/multi-condition query."""
    return user_id in _user_ids_in_room(room_id)

def _add_member(room_id, user_id):
    if not _is_member(room_id, user_id):
        RoomMember.objects.create(room_id=room_id, user_id=user_id)

def _member_usernames(room_id):
    user_ids = _user_ids_in_room(room_id)
    if not user_ids:
        return []
    return list(User.objects.filter(id__in=user_ids).values_list('username', flat=True))

def _dm_display_name(room_id, viewer_id):
    user_ids = _user_ids_in_room(room_id)
    other_ids = [uid for uid in user_ids if uid != viewer_id]
    if not other_ids:
        return 'Unknown'
    user = User.objects.filter(id=other_ids[0]).first()
    return user.username if user else 'Unknown'


# ── room APIs ─────────────────────────────────────────────────────────────────

@login_required
def get_rooms(request):
    user = request.user
    room_ids = _room_ids_for_user(user.id)
    if not room_ids:
        return JsonResponse({'rooms': []})
    rooms = ChatRoom.objects.filter(id__in=room_ids).order_by('-created_at')
    data = []
    for r in rooms:
        last_msg = Message.objects.filter(room_id=r.id).order_by('-created_at').first()
        name = r.name if r.room_type == 'group' else _dm_display_name(r.id, user.id)
        data.append({
            'id':          str(r.id),
            'name':        name,
            'type':        r.room_type,
            'last_msg':    last_msg.text[:60] if last_msg else '',
            'last_sender': last_msg.sender.username if last_msg and last_msg.sender else '',
            'last_time':   last_msg.created_at.strftime('%H:%M') if last_msg else '',
            'members':     _member_usernames(r.id),
        })
    return JsonResponse({'rooms': data})


@login_required
@csrf_exempt
@require_POST
def create_room(request):
    data = json.loads(request.body)
    name = data.get('name', '').strip()
    member_ids = data.get('members', [])
    if not name:
        return JsonResponse({'error': 'Room name is required.'}, status=400)
    room = ChatRoom.objects.create(name=name, room_type='group', created_by=request.user)
    _add_member(room.id, request.user.id)
    for uid in member_ids:
        try:
            uid_int = int(uid)
            if User.objects.filter(id=uid_int).first() is not None:
                _add_member(room.id, uid_int)
        except (ValueError, TypeError):
            pass
    return JsonResponse({'status': 'created', 'id': str(room.id), 'name': room.name})


@login_required
@csrf_exempt
@require_POST
def open_dm(request):
    data   = json.loads(request.body)
    target = get_object_or_404(User, id=int(data['user_id']))
    me     = request.user
    if target.id == me.id:
        return JsonResponse({'error': "Can't DM yourself."}, status=400)
    my_room_ids     = set(_room_ids_for_user(me.id))
    target_room_ids = set(_room_ids_for_user(target.id))
    shared_ids      = list(my_room_ids & target_room_ids)
    existing = None
    if shared_ids:
        existing = ChatRoom.objects.filter(id__in=shared_ids, room_type='direct').first()
    if existing:
        return JsonResponse({'id': str(existing.id), 'name': target.username})
    room = ChatRoom.objects.create(room_type='direct', created_by=me)
    _add_member(room.id, me.id)
    _add_member(room.id, target.id)
    return JsonResponse({'id': str(room.id), 'name': target.username})


# ── message APIs ──────────────────────────────────────────────────────────────

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if not _is_member(room_id, request.user.id):
        return JsonResponse({'error': 'Not a member.'}, status=403)
    after_id = request.GET.get('after')
    qs = Message.objects.filter(room_id=room_id).select_related('sender').order_by('created_at')
    if after_id:
        try:
            qs = qs.filter(id__gt=int(after_id))
        except (ValueError, TypeError):
            pass
    else:
        all_msgs = list(qs)
        qs = all_msgs[-60:]
    data = [{
        'id':      m.id,
        'sender':  m.sender.username if m.sender else 'System',
        'text':    m.text,
        'time':    m.created_at.strftime('%H:%M'),
        'date':    m.created_at.strftime('%d %b %Y'),
        'is_me':   (m.sender_id == request.user.id),
        'initial': m.sender.username[0].upper() if m.sender else '?',
    } for m in qs]
    return JsonResponse({'messages': data})


@login_required
@csrf_exempt
@require_POST
def send_message(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if not _is_member(room_id, request.user.id):
        return JsonResponse({'error': 'Not a member.'}, status=403)
    data = json.loads(request.body)
    text = data.get('text', '').strip()
    if not text:
        return JsonResponse({'error': 'Empty message.'}, status=400)
    msg = Message.objects.create(room=room, sender=request.user, text=text)
    return JsonResponse({
        'id':      msg.id,
        'sender':  msg.sender.username,
        'text':    msg.text,
        'time':    msg.created_at.strftime('%H:%M'),
        'date':    msg.created_at.strftime('%d %b %Y'),
        'is_me':   True,
        'initial': msg.sender.username[0].upper(),
    })


@login_required
def get_users(request):
    users = User.objects.exclude(id=request.user.id).values('id', 'username')
    return JsonResponse({'users': list(users)})
