from xmlrpc.client import Boolean
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms.models import model_to_dict


class TimeLog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name='Start Date')
    end_date = models.DateTimeField(null=True, default=None, verbose_name='End Date')

    def __str__(self):
        str = self.start_date.strftime('%Y-%m-%d %H:%M')
        if (self.end_date is not None):
            str += ' - '
            str += self.end_date.strftime('%Y-%m-%d %H:%M')
        return str

    def json(self):
        return model_to_dict(self)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.BinaryField(blank=True, null=True, verbose_name='API Token', unique=True)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
