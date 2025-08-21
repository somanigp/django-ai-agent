from django.conf import settings
from django.db import models

# Create your models here.

User = settings.AUTH_USER_MODEL  # -> str "auth.User"

# ORM -> Object Relational Mapping
class Document(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Can use SET_NULL, CASCADE, PROTECT, DO_NOTHING, etc.
    title = models.CharField(max_length=300, default='Untitled')
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Auto update on creation.
    updated_at = models.DateTimeField(auto_now=True) # Auto update on every save.