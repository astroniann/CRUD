from django.db import models
from django.contrib.auth.models import User

class EmailCampaign(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    subject = models.CharField(max_length=150)
    body = models.TextField()
    attachment = models.FileField(upload_to="email_attachments", null=True, blank=True)
    sent_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject
