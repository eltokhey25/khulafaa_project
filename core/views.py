from django.shortcuts import get_object_or_404, redirect, render

from .models import Participant
from .utils import normalize_digits


def search(request):
    error = None
    query = ''

    if request.method == 'POST':
        query = request.POST.get('participant_id', '').strip()
        normalized_id = normalize_digits(query)

        if not normalized_id:
            error = 'يرجى إدخال الرقم القومي'
        elif Participant.objects.filter(participant_id=normalized_id).exists():
            return redirect('result', participant_id=normalized_id)
        else:
            error = 'لم يتم العثور على نتيجة لهذا الرقم القومي. تأكد من صحة الرقم وحاول مرة أخرى.'

    return render(request, 'core/search.html', {
        'error': error,
        'query': query,
    })


def result(request, participant_id):
    participant = get_object_or_404(
        Participant,
        participant_id=normalize_digits(participant_id),
    )
    return render(request, 'core/result.html', {
        'participant': participant,
    })
