from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import ReleaseModel, DeletePartsModel, Profile


class ReleaseForm(forms.ModelForm):
    class Meta:
        model = ReleaseModel
        fields = ['id_user', 'default_code', 'massive_changes', 'before_img', 'after_img']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ReleaseForm, self).__init__(*args, **kwargs)
        if user and user.profile.level == 0:
            self.fields['before_img'].required = False
            self.fields['after_img'].required = False
            self.fields.pop('before_img')
            self.fields.pop('after_img')


class DeletePartForm(forms.ModelForm):
    class Meta:
        model = DeletePartsModel
        fields = ['part']


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    level = forms.ChoiceField(choices=[(0, 'Normal User'), (1, 'Admin User')], label="User Level")

    class Meta:
        model = User
        fields = ['username', 'password', 'level']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            Profile.objects.create(user=user, level=self.cleaned_data['level'])
        return user


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
