from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class Meta:
        app_label = 'common'

    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female')
    )

    user = models.OneToOneField(User)
    dob = models.DateField(null=True, blank=True)
    feet = models.IntegerField(null=True, blank=True)
    inches = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True,
                              blank=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True,
                                        null=True)

    def __unicode__(self):
        return self.user.username
