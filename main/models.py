from django.db import models
from django.contrib.auth.models import User
import string
import random


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    unique_id = models.CharField(max_length=8, unique=True, editable=False, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Optionally generate unique_id if needed in the future
        super().save(*args, **kwargs)

    def generate_unique_id(self):
        characters = string.ascii_uppercase + string.digits
        while True:
            unique_id = ''.join(random.choice(characters) for _ in range(8))
            if not UserProfile.objects.filter(unique_id=unique_id).exists():
                return unique_id

    def __str__(self):
        return f"{self.user.username}"


class ChatRoom(models.Model):
    participants = models.ManyToManyField(User, related_name='chat_rooms')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_other_user(self, current_user):
        return self.participants.exclude(id=current_user.id).first()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        users = self.participants.all()
        return f"Chat between {users[0].username if users.count() > 0 else 'Unknown'} and {users[1].username if users.count() > 1 else 'Unknown'}"


class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender.username}: {self.content[:50]}"
