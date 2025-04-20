
from django import forms
from .models import SleepQuestionnaire

class SleepQuestionnaireForm(forms.ModelForm):
    class Meta:
        model = SleepQuestionnaire
        fields = '__all__'
        widgets = {
            'bedtime': forms.TimeInput(attrs={'type': 'time'}),
            'wakeup_time': forms.TimeInput(attrs={'type': 'time'}),
            'time_to_sleep': forms.NumberInput(attrs={'min': 0}),
            'sleep_hours': forms.NumberInput(attrs={'step': 0.5, 'min': 0, 'max': 24}),
            'other_reason': forms.Textarea(attrs={'rows': 3}),
            'partner_other_issues': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make partner-related fields optional initially
        for field in ['partner_snoring', 'partner_breathing_pauses', 
                     'partner_leg_movements', 'partner_confusion',
                     'partner_other_issues', 'partner_other_frequency']:
            self.fields[field].required = False