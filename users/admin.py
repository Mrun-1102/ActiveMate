from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'is_staff', 'get_fitness_goal', 'get_fitness_level')

    def get_fitness_goal(self, obj):
        return obj.profile.get_fitness_goal_display()
    get_fitness_goal.short_description = 'Fitness Goal'

    def get_fitness_level(self, obj):
        return obj.profile.get_fitness_level_display()
    get_fitness_level.short_description = 'Fitness Level'


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
