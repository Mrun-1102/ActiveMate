from django import forms
from .models_activity import DailyActivity, WeightLog

class DailyActivityForm(forms.ModelForm):
    class Meta:
        model = DailyActivity
        fields = ['date', 'steps', 'calories_burned', 'distance_km', 'active_minutes', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

class WeightLogForm(forms.ModelForm):
    class Meta:
        model = WeightLog
        fields = ['date', 'weight', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }