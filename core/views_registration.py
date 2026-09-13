from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms_registration import RegistrationForm
from .models import Participant
from .utils import normalize_digits


def register(request):
    """صفحة تسجيل استمارة المتقدمين."""
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            participant = form.save(commit=False)
            participant.season_year = timezone.now().year
            participant.save()
            return redirect('registration_success', participant_id=participant.participant_id)

    return render(request, 'core/registration.html', {
        'form': form,
    })


def registration_success(request, participant_id):
    """صفحة تأكيد التسجيل."""
    participant = Participant.objects.filter(
        participant_id=participant_id,
    ).order_by('-season_year').first()

    if not participant:
        return redirect('register')

    return render(request, 'core/registration_success.html', {
        'participant': participant,
    })


def registration_print(request, participant_id):
    """صفحة الاستمارة للطباعة."""
    participant = Participant.objects.filter(
        participant_id=participant_id,
    ).order_by('-season_year').first()

    if not participant:
        return redirect('register')

    return render(request, 'core/registration_print.html', {
        'participant': participant,
    })


def participant_history_search(request):
    """صفحة البحث عن سجل طالب."""
    error = None
    participant_id = ''

    if request.method == 'POST':
        participant_id = request.POST.get('participant_id', '').strip()
        normalized = normalize_digits(participant_id)

        if not normalized:
            error = 'يرجى إدخال الرقم القومي'
        elif Participant.objects.filter(participant_id=normalized).exists():
            return redirect('participant_history', participant_id=normalized)
        else:
            error = 'لا توجد سجلات لهذا الرقم القومي.'

    return render(request, 'core/participant_history_search.html', {
        'error': error,
        'participant_id': participant_id,
    })


def participant_history(request, participant_id):
    """صفحة عرض تاريخ المشاركات لطالب."""
    normalized = normalize_digits(participant_id)

    records = Participant.objects.filter(
        participant_id=normalized,
    ).order_by('-season_year')

    if not records.exists():
        return render(request, 'core/participant_history.html', {
            'error': 'لا توجد سجلات لهذا الرقم القومي.',
        })

    return render(request, 'core/participant_history.html', {
        'records': records,
        'participant_id': normalized,
    })
