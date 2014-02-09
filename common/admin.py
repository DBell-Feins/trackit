from django.contrib import admin
import reversion
from models import Goal, UserProfile, WeighIn
# Register your models here.


class GoalAdmin(reversion.VersionAdmin):
    pass


class UserProfileAdmin(reversion.VersionAdmin):
    pass


class WeighInAdmin(reversion.VersionAdmin):
    pass

admin.site.register(Goal, GoalAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(WeighIn, WeighInAdmin)
