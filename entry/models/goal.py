from django.db import models
from django.contrib.auth.models import User


class Goal(models.Model):
    class Meta:
        app_label = 'entry'

    start_date = models.DateField()
    end_date = models.DateField()
    start_weight = models.DecimalField(max_digits=5, decimal_places=2)
    target_weight = models.DecimalField(max_digits=5, decimal_places=2)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'Goal from %s to %s' % (self.start_date, self.end_date)
