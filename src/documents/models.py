from django.conf import settings
from django.db import models
from django.utils import timezone # used to get the current date and time, considering the project’s time zone settings.

# Create your models here.

User = settings.AUTH_USER_MODEL  # -> str "auth.User"

# ORM -> Object Relational Mapping. Table name -> documents_document.
class Document(models.Model):  # app name -> documents, model name -> Document ( add one document at a time )
    # owner will take input of User class obj
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # Can use SET_NULL, CASCADE, PROTECT, DO_NOTHING, etc.
    title = models.CharField(max_length=300, default='Untitled')
    content = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    active_at = models.DateTimeField(auto_now_add=False, auto_now=False, null=True, blank=True)  # This has to have either a null or default value as we added it later, so there is already data added - so that needs to be handled as well.
    # As this is a parameter this .now and not .now().
    # null -> database, None -> python.
    created_at = models.DateTimeField(auto_now_add=True)  # Auto update on creation.
    updated_at = models.DateTimeField(auto_now=True) # Auto update on every save.
    
    def __str__(self) -> str:
        return f"{self.title}"
    
    def save(self, *args, **kwargs):
        # Because active_at in this logic does NOT mean “last time active”.
        # It means: "If the document is currently active, when was it activated?"
        if self.active and self.active_at is None: # Only when reactived should track when was that done.
            self.active_at = timezone.now()
        else:
            self.active_at = None
        super().save(*args, **kwargs) # This is the default behavior of the save method. So making some changes before calling the super method.