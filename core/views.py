from django.shortcuts import render, redirect
from django.contrib import messages
from users.forms import ContactForm
from django.core.mail import send_mail
from django.conf import settings
from fitness.models import WorkoutPlan


def index(request):
    workout_plans = WorkoutPlan.objects.all()[:3]
    context = {
        'workout_plans': workout_plans
    }
    return render(request, 'core/index.html', context)


def about(request):
    return render(request, 'core/about.html')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
         # Construct email message
            email_subject = f"ActiveMate Contact: {subject}"
            email_message = f"From: {name} <{email}>\n\n{message}"
        
        try:
            # Send email
            send_mail(
                email_subject,
                email_message,
                settings.EMAIL_HOST_USER,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent. Thank you!')
        except Exception as e:
            messages.error(request, f'There was an error sending your message. Please try again later.')
        
        return redirect('index')
    
    return redirect('index')

    return render(request, 'core/contact.html', {'form': form})
