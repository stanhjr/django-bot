from django.db import models


class Stock(models.Model):
    text = models.TextField(max_length=3000)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
