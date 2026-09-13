from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
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
    current_year = timezone.now().year
    previous_year = current_year - 1

    qs = Participant.objects.filter(
        season_year__in=[current_year, previous_year]
    ).order_by('-season_year', 'participant_id')

    if query:
        normalized = normalize_digits(query)
        qs = qs.filter(
            Q(name__icontains=query)
            | Q(participant_id__icontains=normalized)
            | Q(participant_id__icontains=query)
        )

    # تجميع السجلات حسب الرقم القومي
    students = {}
    for p in qs:
        pid = p.participant_id
        if pid not in students:
            students[pid] = {
                'participant_id': pid,
                'name': p.name,
                'sheikh_name': p.sheikh_name,
                'phone': p.phone,
                'current': None,
                'previous': None,
                'current_result': None,
                'previous_result': None,
                'current_rank': None,
                'previous_rank': None,
                'current_record_id': None,
                'previous_record_id': None,
            }

        if p.season_year == current_year:
            students[pid]['current'] = p.parts_count
            students[pid]['current_result'] = p.result
            students[pid]['current_rank'] = p.rank
            students[pid]['current_record_id'] = p.id
        elif p.season_year == previous_year:
            students[pid]['previous'] = p.parts_count
            students[pid]['previous_result'] = p.result
            students[pid]['previous_rank'] = p.rank
            students[pid]['previous_record_id'] = p.id

    # إضافة label لعدد الأجزاء
    parts_labels = dict(Participant.PARTS_CHOICES)

    students_list = []
    for s in students.values():
        s['current_label'] = parts_labels.get(s['current'], '—') if s['current'] else '—'
        s['previous_label'] = parts_labels.get(s['previous'], '—') if s['previous'] else '—'
        students_list.append(s)

    students_list.sort(key=lambda x: x['name'])

    return render(request, 'core/manage/dashboard.html', {
        'students': students_list,
        'query': query,
        'current_year': current_year,
        'previous_year': previous_year,
        'total_count': len(students_list),
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
