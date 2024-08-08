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
