from django import forms
from . import models
from datetime import datetime

class FormCandi(forms.ModelForm):

    class Meta:
        model = models.Candidate

        fields=(
            'name',
            'area'
        )

class DateInput(forms.DateInput):
    input_type = 'date'

class FormPoll(forms.ModelForm):

    class Meta:
        model = models.Poll

        # start_date = DateInput()
        # end_date = DateInput()
        fields=(
            'area',
            'start_date',
            'end_date'
        )
        widgets = {
            'start_date': DateInput(),
            'end_date':DateInput(),
        }