from common.api.baseresource import BaseResource
from common.api.exception import CustomBadRequest
from tastypie import fields
from tastypie.models import ApiKey
from tastypie.resources import ALL
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.utils import trailing_slash
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.conf.urls import url


class UserResource(BaseResource):
    goals = fields.ToManyField("common.api.GoalResource", "goal_set",
                               related_name="goal", null=True, blank=True)
    weighins = fields.ToManyField("common.api.WeighInResource", "weighin_set",
                                  related_name="weighin", null=True,
                                  blank=True, full=True)

    def prepend_urls(self):
        return [
            url(r"^login%s$" % trailing_slash(), self.wrap_view('login'),
                name="api_login"),
            url(r'^logout%s$' % trailing_slash(), self.wrap_view('logout'),
                name='api_logout'),
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" %
                self._meta.resource_name, self.wrap_view('dispatch_list'),
                name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" %
                self._meta.resource_name, self.wrap_view('get_schema'),
                name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/set/(?P<pk_list>\w[\w/;-]*)\.(?P<format>\w+)$"
                % self._meta.resource_name,
                self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)\.(?P<format>\w+)$"
                % self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
        ]

    def login(self, request, **kwargs):
        self.method_check(request, allowed=['post'])
        data = self.deserialize(request, request.body,
                                format=request.META.get('CONTENT_TYPE',
                                                        'application/json'))

        username = data.get('username', '')
        password = data.get('password', '')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                api_key, created = ApiKey.objects.get_or_create(user=user)
                if not user.is_authenticated and created is False:
                    api_key.delete()
                    api_key = ApiKey.objects.create(user=user)

                response = self.create_response(request, {
                    'code': 'logged_in',
                    'message': 'You have successfully logged in.',
                    'username': user.username,
                    'key': api_key.key
                })
                return response
            else:
                raise CustomBadRequest(
                    code="account_disabled",
                    message="That account has been disabled.",
                    type=HttpForbidden)
        else:
            raise CustomBadRequest(
                code="username_pass_incorrect",
                message="Username/password incorrect",
                type=HttpUnauthorized)

    def logout(self, request, **kwargs):
        from pdb import set_trace; set_trace()
        self.method_check(request, allowed=['post'])
        if request.user and request.user.is_authenticated():
            try:
                ApiKey.objects.get(user=request.user).delete()
            except ApiKey.DoesNotExist:
                pass
            logout(request)
            return self.create_response(request, {'success': True})
        else:
            return self.create_response(request, {'success': False},
                                        HttpUnauthorized)

    def obj_create(self, bundle, request=None, **kwargs):
        from pdb import set_trace; set_trace()
        return super(UserResource, self).obj_create(bundle,
                                                    user=bundle.request.user)

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request) \
            .filter(pk=request.user.pk)

    class Meta(BaseResource.Meta):
        queryset = User.objects.filter(~Q(id=-1))
        resource_name = "user"
        excludes = ["password", "is_active", "is_staff", "is_superuser"]
        filtering = {
            "username": ALL,
        }
