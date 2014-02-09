from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    class Meta:
        app_label = 'common'

    user = models.ForeignKey(User, unique=True)
    dob = models.DateField()
    height = models.DecimalField(max_digits=4, decimal_places=2)
    gender = models.CharField(max_length=140)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username
