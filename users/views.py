from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Sum
from fitness.models import UserWorkout
from fitness.models_activity import DailyActivity, WeightLog

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Get additional profile data
            phone = request.POST.get('phone')
            fitness_goal = request.POST.get('fitness_goal')
            fitness_level = request.POST.get('fitness_level')
            plan = request.POST.get('plan')

            # Update profile
            profile = user.profile
            if phone:
                profile.phone = phone
            if fitness_goal:
                profile.fitness_goal = fitness_goal
            if fitness_level:
                profile.fitness_level = fitness_level
            if plan:
                profile.plan = plan
            profile.save()

            # Log the user in automatically
            login(request, user)

            username = form.cleaned_data.get('username')
            messages.success(
                request, f'Account created for {username}! Welcome to ActiveMate!')
            return redirect('dashboard')  # Redirect to dashboard
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def dashboard(request):
    # Get user's workout data
    workout_count = 0
    total_minutes = 0
    recent_workouts = []

    # If you have workout models, you can uncomment and modify these lines
    # workout_count = request.user.workouts.count()
    # total_minutes = request.user.workouts.aggregate(Sum('duration'))['duration__sum'] or 0
    # recent_workouts = request.user.workouts.order_by('-date')[:5]
    
    # Get activity data
    
    
    # Get recent activity
    recent_activity = DailyActivity.objects.filter(user=request.user).order_by('-date').first()
    
    # Get weekly stats
    from django.utils import timezone
    today = timezone.now().date()
    week_start = today - timezone.timedelta(days=today.weekday())
    
    weekly_steps = DailyActivity.objects.filter(
        user=request.user, 
        date__gte=week_start,
        date__lte=today
    ).aggregate(Sum('steps'))['steps__sum'] or 0
    
    # Get latest weight
    latest_weight = WeightLog.objects.filter(user=request.user).order_by('-date').first()
    
    context = {
        'workout_count': workout_count,
        'total_minutes': total_minutes,
        'recent_workouts': recent_workouts,
        'recent_activity': recent_activity,
        'weekly_steps': weekly_steps,
        'latest_weight': latest_weight,
    }

    context = {
        'workout_count': workout_count,
        'total_minutes': total_minutes,
        'recent_workouts': recent_workouts,
    }
    return render(request, 'users/dashboard.html', context)
