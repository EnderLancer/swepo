from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Company, Employer, Specific

class NewEmployerForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewEmployerForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            Employer.objects.create(user=user)
        return user

class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ["name", "description"]