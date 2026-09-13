from django.shortcuts import get_object_or_404, redirect, render

from .forms_registration import RegistrationForm
from .models import Participant


def register(request):
    """صفحة تسجيل استمارة المتقدمين."""
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save()
            return redirect('registration_success', participant_id=participant.participant_id)

    return render(request, 'core/registration.html', {
        'form': form,
    })


def registration_success(request, participant_id):
    """صفحة تأكيد التسجيل."""
    participant = get_object_or_404(Participant, participant_id=participant_id)
    return render(request, 'core/registration_success.html', {
        'participant': participant,
    })


def registration_print(request, participant_id):
    """صفحة الاستمارة للطباعة."""
    participant = get_object_or_404(Participant, participant_id=participant_id)
    return render(request, 'core/registration_print.html', {
        'participant': participant,
    })
