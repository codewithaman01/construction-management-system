from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        # ChatRoom — no M2M field
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id',        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name',      models.CharField(blank=True, default='', max_length=100)),
                ('room_type', models.CharField(choices=[('group', 'Group'), ('direct', 'Direct')], default='group', max_length=10)),
                ('created_at',models.DateTimeField(auto_now_add=True)),
                ('created_by',models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                related_name='created_rooms', to=settings.AUTH_USER_MODEL)),
            ],
        ),

        # RoomMember — explicit membership (replaces ManyToManyField)
        migrations.CreateModel(
            name='RoomMember',
            fields=[
                ('id',   models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='memberships', to='chat.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                           related_name='memberships', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('room', 'user')},
            },
        ),

        # Message
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id',        models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text',      models.TextField()),
                ('created_at',models.DateTimeField(auto_now_add=True)),
                ('room',      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                                related_name='messages', to='chat.chatroom')),
                ('sender',    models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL,
                                                to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
            },
        ),
    ]
