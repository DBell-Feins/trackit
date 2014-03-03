from entry.models import WeighIn
from common.api import BaseResource
from tastypie import fields


class WeighInResource(BaseResource):
    goal = fields.ToOneField('common.api.GoalResource', "goal")

    def obj_create(self, bundle, request=None, **kwargs):
        from pdb import set_trace; set_trace()
        return super(WeighInResource, self).obj_create(bundle, user=bundle.request.user)

    class Meta(BaseResource.Meta):
        queryset = WeighIn.objects.all()
        resource_name = "weighin"
