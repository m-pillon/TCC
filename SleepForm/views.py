from django.shortcuts import get_object_or_404, render, redirect
from SleepForm.models import SleepQuestionnaire
from .forms import SleepQuestionnaireForm

def sleep_questionnaire(request):
    if request.method == 'POST':
        form = SleepQuestionnaireForm(request.POST)
        if form.is_valid():
            instance = form.save()
            request.session['latest_questionnaire_id'] = instance.pk  # Store in session
            return redirect('questionnaire_success')  # No PK needed
    else:
        form = SleepQuestionnaireForm()
    
    return render(request, 'SleepForm/questionnaire.html', {'form': form})

def questionnaire_success(request):
    return render(request, 'SleepForm/success.html')