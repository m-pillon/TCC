from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import generic
from .forms import SleepForm  # Import your form class here
from django.urls import reverse_lazy


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def sleep_form_view(request):
    if request.method == 'POST':
        form = SleepForm(request.POST)
        if form.is_valid():
            # Process the form data
            # Example: save to database if you have a model
            # form.save()
            form.save()
            
            # You can access cleaned data like:
            # sleep_quality = form.cleaned_data['sleep_quality']
            # bedtime = form.cleaned_data['bedtime']
            
            # Redirect to a success page or show a message
            return render(request, 'SleepForm/success.html', {
                'message': 'Thank you for submitting your sleep data!'
            })
    else:
        form = SleepForm()  # Create an empty form for GET requests

    return render(request, 'SleepForm/sleep_form.html', {
        'form': form,
        'title': 'Sleep Tracker Form'
    })

def success_view(request):
    return render(request, 'SleepForm/success.html', {
        'message': 'Your form was submitted successfully!'
    })
