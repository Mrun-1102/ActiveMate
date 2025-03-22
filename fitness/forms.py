from django import forms
from .models import UserWorkout, ExerciseLog, WorkoutPlan, WorkoutDay, WorkoutExercise


class UserWorkoutForm(forms.ModelForm):
    class Meta:
        model = UserWorkout
        fields = ['workout_day', 'date',
                  'duration_minutes', 'calories_burned', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }


class ExerciseLogForm(forms.ModelForm):
    class Meta:
        model = ExerciseLog
        fields = ['exercise', 'sets_completed', 'reps_completed', 'weight']


class WorkoutPlanForm(forms.ModelForm):
    class Meta:
        model = WorkoutPlan
        fields = ['name', 'description', 'level', 'goal', 'duration_weeks']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class WorkoutDayForm(forms.ModelForm):
    class Meta:
        model = WorkoutDay
        fields = ['day_number', 'name']


class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'rest_seconds', 'order']
