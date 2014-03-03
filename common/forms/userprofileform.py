from django import forms
import itertools
from django.contrib.auth.models import User
from common.models import UserProfile
from common.forms.widgets import HeightWidget
from django.forms import extras
from django.forms.models import inlineformset_factory


class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(widget=extras.SelectDateWidget(
                          years=range(2014, 1959, -1)),
                          label='Date of birth'
                          )
    feet = forms.IntegerField(widget=forms.Select(choices=itertools.chain(
        [('', '')], ((str(x), x) for x in range(1, 12)))))
    inches = forms.IntegerField(widget=forms.Select(choices=itertools.chain(
        [('', '')], ((str(x), x) for x in range(1, 12)))))

    class Meta:
        model = UserProfile
        widgets = {
            'height': HeightWidget(),
        }


class UserProfileAdminForm(UserProfileForm):
    pass


class UserProfileFormSet(inlineformset_factory(User, UserProfile)):
    def __init__(self, *args, **kwargs):
        super(UserProfileFormSet, self).__init__(*args, **kwargs)
        self.can_delete = False
        self.form = UserProfileAdminForm
