from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Avg, Sum, Max, Min
from .models_activity import DailyActivity, WeightLog
from .forms_activity import DailyActivityForm, WeightLogForm

@login_required
def activity_dashboard(request):
    # Get recent activities
    recent_activities = DailyActivity.objects.filter(user=request.user).order_by('-date')[:7]
    
    # Get weight logs
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-date')[:10]
    
    # Calculate stats
    today = timezone.now().date()
    week_start = today - timezone.timedelta(days=today.weekday())
    month_start = today.replace(day=1)
    
    # Weekly stats
    weekly_activities = DailyActivity.objects.filter(
        user=request.user, 
        date__gte=week_start,
        date__lte=today
    )
    weekly_steps = weekly_activities.aggregate(Sum('steps'))['steps__sum'] or 0
    weekly_calories = weekly_activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    
    # Monthly stats
    monthly_activities = DailyActivity.objects.filter(
        user=request.user, 
        date__gte=month_start,
        date__lte=today
    )
    monthly_steps = monthly_activities.aggregate(Sum('steps'))['steps__sum'] or 0
    monthly_calories = monthly_activities.aggregate(Sum('calories_burned'))['calories_burned__sum'] or 0
    
    # Weight stats
    if weight_logs:
        current_weight = weight_logs.first().weight
        initial_weight = weight_logs.last().weight
        weight_change = current_weight - initial_weight
    else:
        current_weight = None
        weight_change = None
    
    context = {
        'recent_activities': recent_activities,
        'weight_logs': weight_logs,
        'weekly_steps': weekly_steps,
        'weekly_calories': weekly_calories,
        'monthly_steps': monthly_steps,
        'monthly_calories': monthly_calories,
        'current_weight': current_weight,
        'weight_change': weight_change,
    }
    return render(request, 'fitness/activity_dashboard.html', context)

@login_required
def log_activity(request):
    # Check if there's already an activity for today
    today = timezone.now().date()
    existing_activity = DailyActivity.objects.filter(user=request.user, date=today).first()
    
    if request.method == 'POST':
        if existing_activity:
            form = DailyActivityForm(request.POST, instance=existing_activity)
        else:
            form = DailyActivityForm(request.POST)
        
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            messages.success(request, 'Activity logged successfully!')
            return redirect('activity_dashboard')
    else:
        if existing_activity:
            form = DailyActivityForm(instance=existing_activity)
        else:
            form = DailyActivityForm(initial={'date': today})
    
    context = {
        'form': form,
        'is_update': existing_activity is not None
    }
    return render(request, 'fitness/log_activity.html', context)

@login_required
def activity_history(request):
    activities = DailyActivity.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'activities': activities
    }
    return render(request, 'fitness/activity_history.html', context)

@login_required
def edit_activity(request, pk):
    activity = get_object_or_404(DailyActivity, pk=pk, user=request.user)
    
    if request.method == 'POST':
        form = DailyActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Activity updated successfully!')
            return redirect('activity_history')
    else:
        form = DailyActivityForm(instance=activity)
    
    context = {
        'form': form,
        'activity': activity
    }
    return render(request, 'fitness/edit_activity.html', context)

@login_required
def delete_activity(request, pk):
    activity = get_object_or_404(DailyActivity, pk=pk, user=request.user)
    
    if request.method == 'POST':
        activity.delete()
        messages.success(request, 'Activity deleted successfully!')
        return redirect('activity_history')
    
    context = {
        'activity': activity
    }
    return render(request, 'fitness/delete_activity.html', context)

@login_required
def log_weight(request):
    # Check if there's already a weight log for today
    today = timezone.now().date()
    existing_log = WeightLog.objects.filter(user=request.user, date=today).first()
    
    if request.method == 'POST':
        if existing_log:
            form = WeightLogForm(request.POST, instance=existing_log)
        else:
            form = WeightLogForm(request.POST)
        
        if form.is_valid():
            weight_log = form.save(commit=False)
            weight_log.user = request.user
            weight_log.save()
            
            # Update user profile weight
            profile = request.user.profile
            profile.weight = weight_log.weight
            profile.save()
            
            messages.success(request, 'Weight logged successfully!')
            return redirect('activity_dashboard')
    else:
        if existing_log:
            form = WeightLogForm(instance=existing_log)
        else:
            # Pre-fill with user's profile weight if available
            initial_data = {'date': today}
            if request.user.profile.weight:
                initial_data['weight'] = request.user.profile.weight
            form = WeightLogForm(initial=initial_data)
    
    context = {
        'form': form,
        'is_update': existing_log is not None
    }
    return render(request, 'fitness/log_weight.html', context)

@login_required
def weight_history(request):
    weight_logs = WeightLog.objects.filter(user=request.user).order_by('-date')
    
    context = {
        'weight_logs': weight_logs
    }
    return render(request, 'fitness/weight_history.html', context)