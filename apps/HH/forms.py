from django import forms

# from .models import Product
from apps.HH.models import *
from django.forms import inlineformset_factory

class QueryForm(forms.ModelForm):
    class Meta:
        model = Queries
        fields = ['prof']


class QuerySearchForm(forms.ModelForm):

    class Meta:
        model = QuerySearch
        fields = [
            'text',
            # 'specialization',
            'salary_to',
            'area',
            'experience',
            'skill',
            'education',
            'citizenship',
            'work_ticket',
            'age_from',
            'age_to',
            'gender',
            'employment_full',
            'employment_part',
            'employment_project',
            'employment_volunteer',
            'employment_probation',
            'schedule_fullday',
            'schedule_shift',
            'schedule_flexible',
            'schedule_remote',
            'schedule_flyinflyout',
            'language',
            'level'
        ]
        widgets = {
            'text': forms.Textarea(attrs={'rows': 2}),
            'area': forms.Textarea(attrs={'rows': 2}),
            'skill': forms.Textarea(attrs={'rows': 2}),
            'citizenship': forms.Textarea(attrs={'rows': 2}),
            'work_ticket': forms.Textarea(attrs={'rows': 2}),
            'age_from': forms.Textarea(attrs={'rows': 2, }),
            'age_to': forms.Textarea(attrs={'rows': 2, }),
            'language': forms.Textarea(attrs={'rows': 2}),
            'employment_full': forms.CheckboxInput(),
            'employment_part': forms.CheckboxInput(),
            'employment_project': forms.CheckboxInput(),
            'employment_volunteer': forms.CheckboxInput(),
            'employment_probation': forms.CheckboxInput(),

            'schedule_fullday': forms.CheckboxInput(),
            'schedule_shift': forms.CheckboxInput(),
            'schedule_flexible': forms.CheckboxInput(),
            'schedule_remote': forms.CheckboxInput(),
            'schedule_flyinflyout': forms.CheckboxInput(),
        }


