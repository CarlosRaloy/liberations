from django import forms
from django.forms import modelformset_factory
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ReleaseModel, DeletePartsModel, Profile


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = ReleaseModel
        fields = ['default_code', 'massive_changes']

class ReleaseEditForm(forms.ModelForm):
    class Meta:
        model = ReleaseModel
        fields = ['default_code', 'massive_changes', 'before_img', 'after_img']  # Incluye campos adicionales para la edición

class DeletePartForm(forms.ModelForm):
    class Meta:
        model = DeletePartsModel
        fields = ['part']

DeletePartFormSet = modelformset_factory(DeletePartsModel, form=DeletePartForm, extra=1)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    level = forms.ChoiceField(choices=[(0, 'Normal User'), (1, 'Admin User')])

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
