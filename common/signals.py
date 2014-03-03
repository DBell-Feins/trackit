from django.db.models.signals import post_save, pre_save
from tastypie.models import create_api_key, ApiKey
from django.dispatch import receiver
from django.contrib.auth.models import User
from entry.models import Goal, WeighIn


@receiver(pre_save, sender=User)
def generate_api_key(sender, **kwargs):
    user = kwargs['instance']
    try:
        api_key = ApiKey.objects.get(user=user)
    except ApiKey.DoesNotExist:
        api_key = ApiKey.objects.create(user=user)


# @receiver(pre_save, sender=Goal)
# def add_user_to_goal(sender, **kwargs):
#     from pdb import set_trace; set_trace()
#     pass


# @receiver(pre_save, sender=WeighIn)
# def add_user_to_weighin(sender, **kwargs):
#     from pdb import set_trace; set_trace()
#     pass

post_save.connect(create_api_key, sender=User)
