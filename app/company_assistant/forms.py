from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import Company, Employer, ProcessPractice, SwdProcess

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


SCORE = (
    ("W", "Wasn't evaluated"),
    ("N", "Not Achived (0-15%)"),
    ("P", "Partly Achived (16-50%)"),
    ("L", "Largely Achived (50-85%)"),
    ("F", "Fully Achived (86-100%)"),
)


class AttributeForm(forms.Form):
    index = forms.IntegerField(min_value=1, max_value=9)
    name = forms.CharField(required=False)
    score = forms.ChoiceField(choices=SCORE, initial=SCORE[0])

    class Meta:
        fields = ["name", "score"]
        readonly = ["name"]
        widgets = {'index': forms.HiddenInput()}

AttributeFormSet = forms.formset_factory(AttributeForm, extra=0)


def get_attribute_formset():
    attribute_names = {
        1: "Performed",  # PA 1.1
        2: "Performance is managed",  # PA 2.1
        3: "Work product is managed",  # PA 2.2
        4: "Process is defined",  # PA 3.1
        5: "Process is deployed",  # PA 3.2
        6: "Process is measured",  # PA 4.1
        7: "Process is controled",  # PA 4.2
        8: "Process innovation",  # PA 5.1
        9: "Process optimization",  # PA 5.2
    }
    init_params = [
        {
            "index": index,
            "name": name
        }
        for index, name in attribute_names.items()
    ]
    return AttributeFormSet(
        initial=init_params,
    )


class ProcessPracticeFormset(forms.BaseInlineFormSet):
    def add_fields(self, form, index):
        super(ProcessPracticeFormset, self).add_fields(form, index)
        try:
            instance = self.get_queryset()[index]
            pk_value = instance.pk
        except IndexError:
            instance=None
            pk_value = hash(form.prefix)

        attribute_formset = get_attribute_formset()
        attribute_formset.prefix = f'attribute-{pk_value}'
        form.nested = attribute_formset

PracticeFormset = forms.inlineformset_factory(SwdProcess, ProcessPractice,
                                formset=ProcessPracticeFormset, extra=0, fields="__all__")