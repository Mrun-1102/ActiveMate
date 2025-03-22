from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Import activity models
from .models_activity import DailyActivity, WeightLog

class Exercise(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(
        upload_to='exercise_images', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    GOAL_CHOICES = [
        ('weight-loss', 'Weight Loss'),
        ('muscle-gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('general', 'General Fitness'),
    ]

    name = models.CharField(max_length=100, default="Default Workout Plan")
    description = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    goal = models.CharField(max_length=20, choices=GOAL_CHOICES)
    duration_weeks = models.PositiveIntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class WorkoutDay(models.Model):
    workout_plan = models.ForeignKey(
        WorkoutPlan, on_delete=models.CASCADE, related_name='workout_days')
    day_number = models.PositiveIntegerField()
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.workout_plan.name} - Day {self.day_number}: {self.name}"

    class Meta:
        ordering = ['day_number']


class WorkoutExercise(models.Model):
    workout_day = models.ForeignKey(
        WorkoutDay, on_delete=models.CASCADE, related_name='exercises', null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.PositiveIntegerField(default=3)
    reps = models.PositiveIntegerField(default=10)
    rest_seconds = models.PositiveIntegerField(default=60)
    order = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets}x{self.reps}"

    class Meta:
        ordering = ['order']


class UserWorkout(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='workouts')
    workout_day = models.ForeignKey(WorkoutDay, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField()
    calories_burned = models.PositiveIntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout_day.name} - {self.date}"

    class Meta:
        ordering = ['-date']


class ExerciseLog(models.Model):
    user_workout = models.ForeignKey(
        UserWorkout, on_delete=models.CASCADE, related_name='exercise_logs', null=True, blank=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets_completed = models.PositiveIntegerField()
    reps_completed = models.PositiveIntegerField(default=10)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.exercise.name} - {self.sets_completed}x{self.reps_completed}"
