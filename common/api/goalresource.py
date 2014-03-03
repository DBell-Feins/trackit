from common.api import BaseResource
from entry.models import Goal
from tastypie import fields
from tastypie.resources import ALL_WITH_RELATIONS


class GoalResource(BaseResource):
    weighin = fields.ToManyField("common.api.WeighInResource",
                                 "weighin_set",
                                 related_name="goal", full=True, null=True)
    user = fields.ToOneField('common.api.UserResource', "user")

    def obj_create(self, bundle, **kwargs):
        from pdb import set_trace; set_trace()
        return super(GoalResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta(BaseResource.Meta):
        queryset = Goal.objects.all()
        object_class = Goal
        resource_name = "goal"
        allowed_methods = ["delete"] + BaseResource.Meta.allowed_methods
        filtering = {
            "user": ALL_WITH_RELATIONS,
            "start_date": ["exact", "lt", "lte", "gte", "gt"],
            "end_date": ["exact", "lt", "lte", "gte", "gt"],
        }
