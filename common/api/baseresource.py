from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
# from common.api.authenticate import OAuth20Authentication


class BaseResource(ModelResource):
    # def apply_authorization_limits(self, request, object_list):
    #     #if not request.user.is_superuser():
    #         #return object_list.filter(user=request.user)
    #     #else:
    #     return object_list

    class Meta:
        allowed_methods = ["get", "post"]
        authorization = DjangoAuthorization()
        authentication = ApiKeyAuthentication()
