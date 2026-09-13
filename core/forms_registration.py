from django import forms

from .models import Participant
from .utils import normalize_digits


class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('name', 'participant_id', 'sheikh_name', 'phone', 'parts_count')
        labels = {
            'name': 'اسم الطالب',
            'participant_id': 'الرقم القومي',
            'sheikh_name': 'اسم الشيخ المحفظ',
            'phone': 'رقم الهاتف',
            'parts_count': 'عدد الأجزاء',
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثال: أحمد محمد العلي',
                'autocomplete': 'off',
                'autofocus': True,
            }),
            'participant_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': '14 رقمًا',
                'inputmode': 'numeric',
                'maxlength': '14',
                'autocomplete': 'off',
            }),
            'sheikh_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثال: الشيخ عبد الله',
                'autocomplete': 'off',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثال: 01012345678',
                'inputmode': 'tel',
                'maxlength': '15',
                'autocomplete': 'off',
            }),
            'parts_count': forms.Select(attrs={
                'class': 'form-input',
            }),
        }

    def clean_participant_id(self):
        raw = self.cleaned_data['participant_id']
        normalized = normalize_digits(raw)

        if not normalized.isdigit():
            raise forms.ValidationError('الرقم القومي يجب أن يحتوي على أرقام فقط.')

        if len(normalized) != 14:
            raise forms.ValidationError('الرقم القومي يجب أن يكون 14 رقمًا.')

        if Participant.objects.filter(participant_id=normalized).exists():
            raise forms.ValidationError('هذا الرقم القومي مسجّل مسبقًا.')

        return normalized

    def clean_phone(self):
        raw = self.cleaned_data['phone']
        normalized = normalize_digits(raw)

        if not normalized.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')

        if len(normalized) < 7 or len(normalized) > 15:
            raise forms.ValidationError('رقم الهاتف غير صحيح.')

        return normalized

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('الاسم قصير جدًا.')
        return name

    def clean_sheikh_name(self):
        sheikh = self.cleaned_data['sheikh_name'].strip()
        if len(sheikh) < 3:
            raise forms.ValidationError('اسم الشيخ قصير جدًا.')
        return sheikh
