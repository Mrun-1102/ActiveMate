from django.urls import path
from . import views
from . import views_activity

urlpatterns = [
    path('workouts/', views.workout_list, name='workout_list'),
    path('workouts/plan/<int:pk>/', views.workout_plan_detail,
         name='workout_plan_detail'),
    path('workouts/plan/<int:plan_pk>/day/<int:day_pk>/',
         views.workout_day_detail, name='workout_day_detail'),
    path('workouts/start/<int:day_pk>/',
         views.start_workout, name='start_workout'),
    path('workouts/history/', views.workout_history, name='workout_history'),
    path('workouts/history/<int:pk>/',
         views.workout_detail, name='workout_detail'),
    path('workouts/history/<int:pk>/edit/',
         views.edit_workout, name='edit_workout'),
    path('workouts/history/<int:pk>/delete/',
         views.delete_workout, name='delete_workout'),
    path('workout-plans/', views.workout_plans, name='workout_plans'),


    # Admin routes
    path('workouts/plan/create/', views.create_workout_plan,
         name='create_workout_plan'),
    path('workouts/plan/<int:pk>/edit/',
         views.edit_workout_plan, name='edit_workout_plan'),
    path('workouts/plan/<int:pk>/delete/',
         views.delete_workout_plan, name='delete_workout_plan'),
    path('workouts/plan/<int:plan_pk>/day/add/',
         views.add_workout_day, name='add_workout_day'),
    path('workouts/plan/<int:plan_pk>/day/<int:day_pk>/edit/',
         views.edit_workout_day, name='edit_workout_day'),
    path('workouts/plan/<int:plan_pk>/day/<int:day_pk>/delete/',
         views.delete_workout_day, name='delete_workout_day'),
    path('workouts/day/<int:day_pk>/exercise/add/',
         views.add_exercise, name='add_exercise'),

     # Activity tracking URLs
    path('activity/', views_activity.activity_dashboard, name='activity_dashboard'),
    path('activity/log/', views_activity.log_activity, name='log_activity'),
    path('activity/history/', views_activity.activity_history, name='activity_history'),
    path('activity/edit/<int:pk>/', views_activity.edit_activity, name='edit_activity'),
    path('activity/delete/<int:pk>/', views_activity.delete_activity, name='delete_activity'),
    path('weight/log/', views_activity.log_weight, name='log_weight'),
    path('weight/history/', views_activity.weight_history, name='weight_history'),
]
