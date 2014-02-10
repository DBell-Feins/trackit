from django import forms
from common.models import UserProfile
from common.forms.widgets import HeightWidget
from django.forms import extras


class UserProfileField(forms.ModelForm):
    class Meta:
        model = UserProfile
        widgets = {
            'dob': extras.SelectDateWidget(years=range(1960, 2014)),
        }
        labels = {
            'dob': 'Date of birth',
        }


class UserProfileForm(UserProfileField):
    class Meta:
        widgets = {
            'height': HeightWidget()
        }


class UserProfileAdminForm(UserProfileField):
    pass
