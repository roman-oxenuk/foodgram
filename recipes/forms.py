from django import forms
from django.forms.widgets import CheckboxSelectMultiple

from .models import Tag



class TagsFilterForm(forms.Form):

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=CheckboxSelectMultiple(),
        to_field_name='name'
    )
