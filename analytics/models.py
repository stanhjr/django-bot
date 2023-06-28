from django.db import models


class TelegramUsers(models.Model):
    telegram_id = models.BigIntegerField()

    def __str__(self):
        return f'{self.telegram_id}'

    @classmethod
    def set_user_id(cls, telegram_id):
        instance, _ = cls.objects.get_or_create(telegram_id=telegram_id)
        return instance


class Analytics(models.Model):
    users_unique = models.BigIntegerField(default=0)
    number_of_clicks = models.BigIntegerField(default=0)

    def __str__(self):
        return 'Analytics'

    @classmethod
    def set_analytics(cls, telegram_id):
        TelegramUsers.set_user_id(telegram_id=telegram_id)
        instance = cls.objects.first()
        if not instance:
            instance = cls.objects.create()
        instance.users_unique = TelegramUsers.objects.count()
        instance.number_of_clicks += 1
        instance.save()
