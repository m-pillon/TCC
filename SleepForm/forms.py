from django import forms

class SleepForm(forms.Form):
    bedtime = forms.TimeField(label='What time did you go to bed?')
    wakeup_time = forms.TimeField(label='What time did you wake up?')
    sleep_quality = forms.IntegerField(
        label='Rate your sleep quality (1-10)',
        min_value=1,
        max_value=10
    )
    notes = forms.CharField(
        label='Additional notes',
        widget=forms.Textarea,
        required=False
    )