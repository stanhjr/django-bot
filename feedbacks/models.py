from django.db import models


class Feedback(models.Model):
    text = models.TextField(max_length=1000)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        created_at_formatted = self.created_at.strftime("%Y-%m-%d %H:%M:%S")
        return f'{created_at_formatted} {self.is_read}'
