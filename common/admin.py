from django.contrib import admin
from django.contrib.auth.models import User
from reversion.admin import VersionAdmin
from tastypie.admin import ApiKeyInline
from guardian.admin import GuardedModelAdmin
from common.models import UserProfile
from entry.models import WeighIn, Goal
from common.forms.userprofileform import UserProfileFormSet

# Register your models here.
admin.site.unregister(User)


class WeighInInline(admin.TabularInline):
    model = WeighIn
    extra = 0

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        field = super(WeighInInline, self).formfield_for_foreignkey(
            db_field, request, **kwargs)
        if db_field.name == 'user':
            if request._goal_user_ is not None:
                field.initial = request._goal_user_
                field.queryset = field.queryset.filter(
                    username__exact=request._goal_user_)
            else:
                field.queryset = field.queryset.none()
        return field


class GoalInline(admin.TabularInline):
    model = Goal
    extra = 0


class GoalAdmin(VersionAdmin, GuardedModelAdmin):
    inlines = [WeighInInline]
    user_can_access_owned_objects_only = True

    def get_form(self, request, obj=None, **kwargs):
        # just save obj reference for future processing in Inline
        request._goal_user_ = obj.user if obj is not None else None
        return super(GoalAdmin, self).get_form(request, obj, **kwargs)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = 'user'
    max_num = 1
    formset = UserProfileFormSet


class ApiKeyInlineOverload(ApiKeyInline):
    readonly_fields = ('key', 'created')
    max_num = 1


class UserProfileAdmin(VersionAdmin, GuardedModelAdmin):
    inlines = [UserProfileInline, ApiKeyInlineOverload, GoalInline]
    user_can_access_owned_objects_only = True
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined',
                   'last_login']
    list_display = ['first_name', 'last_name', 'email', 'username',
                    'date_joined']
    list_display_links = ['first_name', 'last_name', 'email', 'username']


admin.site.register(Goal, GoalAdmin)
admin.site.register(User, UserProfileAdmin)
