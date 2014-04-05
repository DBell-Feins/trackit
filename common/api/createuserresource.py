from tastypie.resources import Resource, Bundle
from common.api.exception import CustomBadRequest
from tastypie.http import HttpUnauthorized, HttpForbidden
from tastypie.http import HttpBadRequest
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.authentication import Authentication
from django.db import IntegrityError
from django.contrib.auth.models import User
from django.conf.urls import url
from django.core.urlresolvers import reverse
from registration.models import RegistrationProfile


class UserObject(object):
    def __init__(self, initial=None):
        self.__dict__['_data'] = {}

        if hasattr(initial, 'items'):
            self.__dict__['_data'] = initial

    def __getattr__(self, name):
        return self._data.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__['_data'][name] = value

    def to_dict(self):
        return self._data


class CreateUserResource(Resource):
    activation_key = fields.CharField(attribute='activation_key', blank=True,
                                      null=True)
    user = fields.ToOneField('common.api.UserResource', "user")

    def _reg_profile(self):
        return RegistrationProfile()

    def detail_uri_kwargs(self, bundle_or_obj):
        kwargs = {}
        from pdb import set_trace; set_trace()
        if isinstance(bundle_or_obj, Bundle):
            kwargs['pk'] = bundle_or_obj.obj.id
        else:
            kwargs['pk'] = bundle_or_obj.id

        return kwargs

    def get_object_list(self, request):
        reg_profiles = self._reg_profile().objects

        # results = []
        # for profile in reg_profiles:
        #     new_obj = UserObject
        from pdb import set_trace; set_trace()
        pass

    def obj_get_list(self, bundle, **kwargs):
        from pdb import set_trace; set_trace()
        raise CustomBadRequest(
            code="account_disabled",
            message="That account has been disabled.",
            type=HttpForbidden)

    def obj_get(self, bundle, **kwargs):
        registration = RegistrationProfile.objects.get(
            activation_key=kwargs['pk'])
        self.user = registration.user
        self.activation_key = registration.activation_key
        return self

    def obj_create(self, bundle, **kwargs):
        self.method_check(bundle.request, allowed=['post'])
        username = bundle.data.get('username', '')
        password = bundle.data.get('password', '')
        email = bundle.data.get('email', '')
        resp = {}
        resp = {"code": "invalid_password",
                "message": "A password must be supplied."} if \
            password == '' else {"code": "invalid_email",
                        "message": "An email address must be supplied."} if \
            email == '' else {}

        if resp != {}:
            raise CustomBadRequest(
                code=resp['code'],
                message=resp['message'],
                type=HttpBadRequest)
        try:
            new_user = RegistrationProfile.objects.create_inactive_user(
                username=username,
                password=password,
                email=email, site="", send_email=False)
        except IntegrityError:
            raise CustomBadRequest(
                code="account_exists",
                message="That account already exists.",
                type=HttpBadRequest)
        except ValueError as e:
            raise CustomBadRequest(
                code="value_error",
                message=e.args[0],
                type=HttpBadRequest)

        new_user_registration = RegistrationProfile.objects.get(user=new_user)
        from pdb import set_trace; set_trace()
        bundle.obj = new_user_registration
        bundle = self.full_hydrate(bundle)
        return bundle
        # self.activation_key = new_user_registration.activation_key

        # response = self.create_response(bundle.request, {
        #     'code': 'registered',
        #     'message': 'You have successfully registered.',
        #     'username': new_user.username,
        #     'activation_key': new_user_registration.activation_key,
        #     })
        # return response

    def obj_update(self, bundle, **kwargs):
        return self.obj_create(bundle, **kwargs)

    def obj_delete_list(self, bundle, **kwargs):
        pass

    def obj_delete(self, bundle, **kwargs):
        pass

    def rollback(self, bundles):
        pass

    class Meta:
        resource_name = 'register'
        object_class = UserObject
        authorization = Authorization()
        # allowed_methods = ['post', 'get']
        # always_return_data = True
        # excludes = ["password", "resource_uri"]
        # authentication = Authentication()
