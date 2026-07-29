from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ManageLoginForm, ParticipantForm
from .models import Participant
from .utils import normalize_digits


def staff_required(view_func):
    return login_required(
        user_passes_test(lambda user: user.is_staff)(view_func),
        login_url='manage_login',
    )


def manage_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('manage_dashboard')

    form = ManageLoginForm()
    error = None

    if request.method == 'POST':
        form = ManageLoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
            )
            if user is not None and user.is_staff:
                login(request, user)
                return redirect('manage_dashboard')
            error = 'بيانات الدخول غير صحيحة أو ليس لديك صلاحية الوصول.'

    return render(request, 'core/manage/login.html', {
        'form': form,
        'error': error,
    })


@staff_required
def manage_logout(request):
    logout(request)
    messages.success(request, 'تم تسجيل الخروج بنجاح.')
    return redirect('manage_login')


@staff_required
def manage_dashboard(request):
    query = request.GET.get('q', '').strip()
    participants = Participant.objects.all()

    if query:
        normalized = normalize_digits(query)
        participants = participants.filter(
            Q(name__icontains=query)
            | Q(participant_id__icontains=normalized)
            | Q(participant_id__icontains=query)
        )

    return render(request, 'core/manage/dashboard.html', {
        'participants': participants,
        'query': query,
        'total_count': Participant.objects.count(),
    })


@staff_required
def manage_add(request):
    form = ParticipantForm()

    if request.method == 'POST':
        form = ParticipantForm(request.POST)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'تم إضافة {participant.name} بنجاح.')
            return redirect('manage_dashboard')

    return render(request, 'core/manage/form.html', {
        'form': form,
        'title': 'إضافة طالب',
        'submit_label': 'حفظ الطالب',
    })


@staff_required
def manage_edit(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    form = ParticipantForm(instance=participant)

    if request.method == 'POST':
        form = ParticipantForm(request.POST, instance=participant)
        if form.is_valid():
            participant = form.save()
            messages.success(request, f'تم تحديث بيانات {participant.name} بنجاح.')
            return redirect('manage_dashboard')

    return render(request, 'core/manage/form.html', {
        'form': form,
        'participant': participant,
        'title': 'تعديل بيانات الطالب',
        'submit_label': 'حفظ التعديلات',
    })


@staff_required
@require_POST
def manage_delete(request, pk):
    participant = get_object_or_404(Participant, pk=pk)
    name = participant.name
    participant.delete()
    messages.success(request, f'تم حذف {name} بنجاح.')
    return redirect('manage_dashboard')
