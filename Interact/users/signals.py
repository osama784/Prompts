from django.db.models.signals import post_save, post_delete, pre_save
from django.contrib.auth.models import User
from .models import Profile


def deleteUser(sender, instance, **kwrgs):
    user = instance.owner
    user.delete()





post_delete.connect(deleteUser, sender=Profile)


