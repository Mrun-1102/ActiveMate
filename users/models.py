
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone


class Profile(models.Model):
    GOAL_CHOICES = [
        ('weight-loss', 'Weight Loss'),
        ('muscle-gain', 'Muscle Gain'),
        ('endurance', 'Endurance'),
        ('flexibility', 'Flexibility'),
        ('general', 'General Fitness'),
    ]

    LEVEL_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    PLAN_CHOICES = [
        ('free', 'Free Trial'),
        ('basic', 'Basic Plan'),
        ('premium', 'Premium Plan'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone = models.CharField(max_length=15, blank=True, null=True, default="")
    fitness_goal = models.CharField(
        max_length=20, choices=GOAL_CHOICES, blank=True, null="General Fitness")
    fitness_level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, blank=True, null=True, default='beginner')
    plan = models.CharField(
        max_length=20, choices=PLAN_CHOICES, default='free')

    
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Weight in kg")
    age = models.PositiveIntegerField(null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        # Resize profile image if needed
        if self.image:
            try:
                img = Image.open(self.image.path)
                if img.height > 300 or img.width > 300:
                    output_size = (300, 300)
                    img.thumbnail(output_size)
                    img.save(self.image.path)
            except (FileNotFoundError, ValueError):
                # Handle case where image file doesn't exist yet
                pass
    
    def calculate_bmi(self):
        """Calculate BMI if height and weight are available"""
        if self.height and self.weight and self.height > 0:
            # Convert height from cm to m
            height_m = self.height / 100
            return round(self.weight / (height_m * height_m), 1)
        return None
    
    def calculate_age(self):
        """Calculate age from date of birth"""
        if self.date_of_birth:
            today = timezone.now().date()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return self.age
