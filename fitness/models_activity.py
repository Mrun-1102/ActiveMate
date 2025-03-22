from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class DailyActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_activities')
    date = models.DateField(default=timezone.now)
    steps = models.PositiveIntegerField(default=0)
    calories_burned = models.PositiveIntegerField(default=0)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    active_minutes = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
        verbose_name_plural = 'Daily Activities'
    
    def __str__(self):
        return f"{self.user.username}'s activity on {self.date}"

class WeightLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weight_logs')
    date = models.DateField(default=timezone.now)
    weight = models.DecimalField(max_digits=5, decimal_places=2, help_text="Weight in kg")
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']
    
    def __str__(self):
        return f"{self.user.username}'s weight on {self.date}: {self.weight} kg"