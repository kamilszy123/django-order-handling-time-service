from django.utils import timezone
from datetime import timedelta

from django.db import models

class Account(models.Model):
    name = models.CharField(max_length=100, unique=True)

    access_token = models.TextField(null=True, blank=True)
    refresh_token = models.TextField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def is_token_expired(self):
        if not self.expires_at:
            return True
        return self.expires_at < timezone.now() + timedelta(seconds=30)

    def __str__(self):
        return self.name


class HandlingTimeConfig(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    offer_id = models.CharField(max_length=100, unique=True)
    target_date = models.DateField()

    def __str__(self):
        return f"{self.offer_id} -> {self.target_date}"
