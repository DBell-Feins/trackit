from common.api.baseresource import BaseResource
from tastypie import fields
from django.contrib.auth.models import User
from tastypie.resources import ALL
from django.db.models import Q


class UserResource(BaseResource):
    goals = fields.ToManyField("common.api.GoalResource", "goal_set",
                               related_name="goal", null=True, blank=True)
    weighins = fields.ToManyField("common.api.WeighInResource", "weighin_set",
                                  related_name="weighin", null=True,
                                  blank=True, full=True)

    def obj_create(self, bundle, request=None, **kwargs):
        from pdb import set_trace; set_trace()
        return super(UserResource, self).obj_create(bundle, user=bundle.request.user)

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request).filter(pk=request.user.pk)

    class Meta(BaseResource.Meta):
        # queryset = User.objects.all()
        queryset = User.objects.filter(~Q(id=-1))
        resource_name = "user"
        excludes = ["password", "is_active", "is_staff", "is_superuser"]
        filtering = {
            "username": ALL,
        }
