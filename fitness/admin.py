from django.contrib import admin
from .models import Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise, UserWorkout, ExerciseLog
from .models_activity import DailyActivity, WeightLog

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)


class WorkoutExerciseInline(admin.TabularInline):
    model = WorkoutExercise
    extra = 1


@admin.register(WorkoutDay)
class WorkoutDayAdmin(admin.ModelAdmin):
    list_display = ('name', 'workout_plan', 'day_number')
    list_filter = ('workout_plan',)
    search_fields = ('name',)
    inlines = [WorkoutExerciseInline]


@admin.register(WorkoutPlan)
class WorkoutPlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'goal', 'duration_weeks')
    list_filter = ('level', 'goal')
    search_fields = ('name', 'description')


class ExerciseLogInline(admin.TabularInline):
    model = ExerciseLog
    extra = 1


@admin.register(UserWorkout)
class UserWorkoutAdmin(admin.ModelAdmin):
    list_display = ('user', 'workout_day', 'date',
                    'duration_minutes', 'calories_burned')
    list_filter = ('user', 'date')
    search_fields = ('user__username', 'workout_day__name')
    inlines = [ExerciseLogInline]


@admin.register(ExerciseLog)
class ExerciseLogAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'user_workout',
                    'sets_completed', 'reps_completed', 'weight')
    list_filter = ('exercise', 'user_workout__user')


@admin.register(DailyActivity)
class DailyActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'steps', 'calories_burned', 'distance_km', 'active_minutes')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)

@admin.register(WeightLog)
class WeightLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight')
    list_filter = ('user', 'date')
    search_fields = ('user__username',)
