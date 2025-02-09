from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from cities_light.models import City
from django.utils.translation import gettext_lazy as _


class SingUpForm(UserCreationForm):

    city = forms.ModelChoiceField(City.objects.all(), widget=forms.HiddenInput())
    email = forms.EmailField(required=False, help_text=_("Email not required"))
    class Meta:
        model = User
        fields = ("username", _("email"), "city", "password1", "password2")


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["paypal_email", "about", "company_name", "ProfileImg"]
