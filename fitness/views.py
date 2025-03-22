from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Exercise, WorkoutPlan, WorkoutDay, WorkoutExercise, UserWorkout, ExerciseLog
from .forms import UserWorkoutForm, ExerciseLogForm, WorkoutPlanForm, WorkoutDayForm, WorkoutExerciseForm


@login_required
def workout_list(request):
    workout_plans = WorkoutPlan.objects.all()
    user_workouts = UserWorkout.objects.filter(
        user=request.user).order_by('-date')

    context = {
        'workout_plans': workout_plans,
        'user_workouts': user_workouts,
    }
    return render(request, 'fitness/workout_list.html', context)

@login_required
def workout_plans(request):
    """View to display workout plans - accessible to all users"""
    workout_plans = WorkoutPlan.objects.all()
    
    # For authenticated users, we can show personalized recommendations
    if request.user.is_authenticated:
        try:
            user_level = request.user.profile.fitness_level
            recommended_plans = WorkoutPlan.objects.filter(fitness_level=user_level)
        except:
            recommended_plans = []
    else:
        recommended_plans = []
        user_level = None
    
    context = {
        'workout_plans': workout_plans,
        'recommended_plans': recommended_plans,
        'user_level': user_level
    }
    return render(request, 'fitness/workout_plans.html', context)

@login_required
def workout_plan_detail(request, pk):
    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)
    workout_days = workout_plan.workout_days.all()

    context = {
        'workout_plan': workout_plan,
        'workout_days': workout_days,
    }
    return render(request, 'fitness/workout_plan_detail.html', context)


@login_required
def workout_day_detail(request, plan_pk, day_pk):
    workout_day = get_object_or_404(
        WorkoutDay, pk=day_pk, workout_plan__pk=plan_pk)
    exercises = workout_day.exercises.all()

    context = {
        'workout_day': workout_day,
        'exercises': exercises,
    }
    return render(request, 'fitness/workout_day_detail.html', context)


@login_required
def start_workout(request, day_pk):
    workout_day = get_object_or_404(WorkoutDay, pk=day_pk)
    exercises = workout_day.exercises.all()

    if request.method == 'POST':
        form = UserWorkoutForm(request.POST)
        if form.is_valid():
            user_workout = form.save(commit=False)
            user_workout.user = request.user
            user_workout.workout_day = workout_day
            user_workout.save()

            # Save exercise logs
            for exercise in exercises:
                sets = request.POST.get(f'sets_{exercise.id}')
                reps = request.POST.get(f'reps_{exercise.id}')
                weight = request.POST.get(f'weight_{exercise.id}')

                if sets and reps:
                    ExerciseLog.objects.create(
                        user_workout=user_workout,
                        exercise=exercise.exercise,
                        sets_completed=sets,
                        reps_completed=reps,
                        weight=weight if weight else None
                    )

            messages.success(request, 'Workout logged successfully!')
            return redirect('workout_history')
    else:
        form = UserWorkoutForm(initial={'workout_day': workout_day})

    context = {
        'workout_day': workout_day,
        'exercises': exercises,
        'form': form,
    }
    return render(request, 'fitness/start_workout.html', context)


@login_required
def workout_history(request):
    user_workouts = UserWorkout.objects.filter(
        user=request.user).order_by('-date')

    context = {
        'user_workouts': user_workouts,
    }
    return render(request, 'fitness/workout_history.html', context)


@login_required
def workout_detail(request, pk):
    user_workout = get_object_or_404(UserWorkout, pk=pk, user=request.user)
    exercise_logs = user_workout.exercise_logs.all()

    context = {
        'user_workout': user_workout,
        'exercise_logs': exercise_logs,
    }
    return render(request, 'fitness/workout_detail.html', context)


@login_required
def edit_workout(request, pk):
    user_workout = get_object_or_404(UserWorkout, pk=pk, user=request.user)
    exercise_logs = user_workout.exercise_logs.all()

    if request.method == 'POST':
        form = UserWorkoutForm(request.POST, instance=user_workout)
        if form.is_valid():
            form.save()

            # Update exercise logs
            for log in exercise_logs:
                sets = request.POST.get(f'sets_{log.id}')
                reps = request.POST.get(f'reps_{log.id}')
                weight = request.POST.get(f'weight_{log.id}')

                if sets and reps:
                    log.sets_completed = sets
                    log.reps_completed = reps
                    log.weight = weight if weight else None
                    log.save()

            messages.success(request, 'Workout updated successfully!')
            return redirect('workout_detail', pk=user_workout.pk)
    else:
        form = UserWorkoutForm(instance=user_workout)

    context = {
        'form': form,
        'user_workout': user_workout,
        'exercise_logs': exercise_logs,
    }
    return render(request, 'fitness/edit_workout.html', context)


@login_required
def delete_workout(request, pk):
    user_workout = get_object_or_404(UserWorkout, pk=pk, user=request.user)

    if request.method == 'POST':
        user_workout.delete()
        messages.success(request, 'Workout deleted successfully!')
        return redirect('workout_history')

    context = {
        'user_workout': user_workout,
    }
    return render(request, 'fitness/delete_workout.html', context)

# Admin views for workout plans


@login_required
def create_workout_plan(request):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST)
        if form.is_valid():
            workout_plan = form.save()
            messages.success(request, 'Workout plan created successfully!')
            return redirect('workout_plan_detail', pk=workout_plan.pk)
    else:
        form = WorkoutPlanForm()

    context = {
        'form': form,
        'title': 'Create Workout Plan',
    }
    return render(request, 'fitness/workout_plan_form.html', context)


@login_required
def edit_workout_plan(request, pk):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)

    if request.method == 'POST':
        form = WorkoutPlanForm(request.POST, instance=workout_plan)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout plan updated successfully!')
            return redirect('workout_plan_detail', pk=workout_plan.pk)
    else:
        form = WorkoutPlanForm(instance=workout_plan)

    context = {
        'form': form,
        'title': 'Edit Workout Plan',
    }
    return render(request, 'fitness/workout_plan_form.html', context)


@login_required
def delete_workout_plan(request, pk):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    workout_plan = get_object_or_404(WorkoutPlan, pk=pk)

    if request.method == 'POST':
        workout_plan.delete()
        messages.success(request, 'Workout plan deleted successfully!')
        return redirect('workout_list')

    context = {
        'workout_plan': workout_plan,
    }
    return render(request, 'fitness/delete_workout_plan.html', context)


@login_required
def add_workout_day(request, plan_pk):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    workout_plan = get_object_or_404(WorkoutPlan, pk=plan_pk)

    if request.method == 'POST':
        form = WorkoutDayForm(request.POST)
        if form.is_valid():
            workout_day = form.save(commit=False)
            workout_day.workout_plan = workout_plan
            workout_day.save()
            messages.success(request, 'Workout day added successfully!')
            return redirect('workout_plan_detail', pk=plan_pk)
    else:
        form = WorkoutDayForm()

    context = {
        'form': form,
        'workout_plan': workout_plan,
        'title': 'Add Workout Day',
    }
    return render(request, 'fitness/workout_day_form.html', context)


@login_required
def edit_workout_day(request, plan_pk, day_pk):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    workout_day = get_object_or_404(
        WorkoutDay, pk=day_pk, workout_plan__pk=plan_pk)

    if request.method == 'POST':
        form = WorkoutDayForm(request.POST, instance=workout_day)
        if form.is_valid():
            form.save()
            messages.success(request, 'Workout day updated successfully!')
            return redirect('workout_day_detail', plan_pk=plan_pk, day_pk=day_pk)
    else:
        form = WorkoutDayForm(instance=workout_day)

    context = {
        'form': form,
        'workout_day': workout_day,
        'title': 'Edit Workout Day',
    }
    return render(request, 'fitness/workout_day_form.html', context)


@login_required
def delete_workout_day(request, plan_pk, day_pk):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    workout_day = get_object_or_404(
        WorkoutDay, pk=day_pk, workout_plan__pk=plan_pk)

    if request.method == 'POST':
        workout_day.delete()
        messages.success(request, 'Workout day deleted successfully!')
        return redirect('workout_plan_detail', pk=plan_pk)

    context = {
        'workout_day': workout_day,
    }
    return render(request, 'fitness/delete_workout_day.html', context)


@login_required
def add_exercise(request, day_pk):
    if not request.user.is_staff:
        messages.error(
            request, 'You do not have permission to access this page.')
        return redirect('dashboard')

    workout_day = get_object_or_404(WorkoutDay, pk=day_pk)

    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            workout_exercise = form.save(commit=False)
            workout_exercise.workout_day = workout_day
            workout_exercise.save()
            messages.success(request, 'Exercise added successfully!')
            return redirect('workout_day_detail', plan_pk=workout_day.workout_plan.pk, day_pk=day_pk)
    else:
        form = WorkoutExerciseForm()

    context = {
        'form': form,
        'workout_day': workout_day,
        'title': 'Add Exercise',
    }
    return render(request, 'fitness/workout_exercise_form.html', context)
