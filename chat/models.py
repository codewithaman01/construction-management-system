from django.db import models
from accounts.models import User


class ChatRoom(models.Model):
    """A chat room — either a group room or a 1-on-1 DM.

    NOTE: We use an explicit RoomMember model instead of ManyToManyField
    because djongo (MongoDB) cannot handle M2M INNER JOIN queries.
    """

    ROOM_TYPES = [
        ('group',  'Group'),
        ('direct', 'Direct'),
    ]

    name        = models.CharField(max_length=100, blank=True, default='')
    room_type   = models.CharField(max_length=10, choices=ROOM_TYPES, default='group')
    created_by  = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_rooms')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f'DM-{self.id}'


class RoomMember(models.Model):
    """Explicit membership table — replaces M2M to avoid djongo JOIN bugs."""
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='memberships')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')

    class Meta:
        unique_together = ('room', 'user')

    def __str__(self):
        return f'{self.user} in {self.room}'


class Message(models.Model):
    room       = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender     = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text       = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.sender}: {self.text[:40]}'
