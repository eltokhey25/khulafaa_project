from django.shortcuts import render

from .forms_registration import RegistrationForm


def register(request):
    """صفحة تسجيل استمارة المتقدمين."""
    form = RegistrationForm()
    success = False

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            success = True
            form = RegistrationForm()  # فورم فاضي بعد النجاح

    return render(request, 'core/registration.html', {
        'form': form,
        'success': success,
    })
