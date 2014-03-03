from django.db import models
from django.contrib.auth.models import User


class WeighIn(models.Model):
    class Meta:
        app_label = 'entry'
        verbose_name_plural = "Weigh-ins"

    weight = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.DateField()
    user = models.ForeignKey(User)
    goal = models.ForeignKey('Goal', null=True, blank=True)

    def __unicode__(self):
        return 'User weighed %s pounds on %s' % (self.weight, self.date)
