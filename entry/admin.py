from django.contrib import admin
import reversion
from models import WeighIn

# Register your models here.


class WeighInAdmin(reversion.VersionAdmin):
    pass

admin.site.register(WeighIn, WeighInAdmin)
