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
    dob = models.DateField()
    feet = models.IntegerField()
    inches = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=False)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    def __unicode__(self):
        return self.user.username
