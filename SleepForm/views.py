from django.shortcuts import get_object_or_404, render, redirect
from SleepForm.models import SleepQuestionnaire
from .forms import SleepQuestionnaireForm

def sleep_questionnaire(request):
    if request.method == 'POST':
        form = SleepQuestionnaireForm(request.POST)
        if form.is_valid():
            instance = form.save()
            request.session['latest_questionnaire_id'] = instance.pk  # Store the ID of the latest questionnaire in the session
            return redirect('questionnaire_success') 
    else:
        form = SleepQuestionnaireForm()
    
    return render(request, 'SleepForm/questionnaire.html', {'form': form})

def questionnaire_success(request):
    # return render(request, 'SleepForm/success.html')

    pk = request.session.get('latest_questionnaire_id')
    if not pk:
        return redirect('sleep_questionnaire')  # Fallback if no session
    
    record = get_object_or_404(SleepQuestionnaire, pk=pk)
    return render(request, 'SleepForm/success.html', {'scores': record.calculate_total_score()})