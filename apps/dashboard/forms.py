from django import forms
from apps.accounts.models import *

class PlanForm(forms.ModelForm):

    class Meta:
        model = SubscriptionPlan
        fields = ['title', 'post_requirement', 'view_requirement', 'view_contact', 'show_interest',
                  'contact', 'free_plan']

    def __init__(self, *args, **kwargs):

        super(PlanForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'input-xlarge'
        self.fields['post_requirement'].widget.attrs['class'] = 'input-xlarge'
        self.fields['view_requirement'].widget.attrs['class'] = 'input-xlarge'
        self.fields['view_contact'].widget.attrs['class'] = 'input-xlarge'
        self.fields['show_interest'].widget.attrs['class'] = 'input-xlarge'