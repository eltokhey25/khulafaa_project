from django import forms

from .models import Participant
from .utils import normalize_digits


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('name', 'participant_id', 'sheikh_name', 'phone', 'parts_count', 'season_year', 'result', 'rank')
        labels = {
            'name': 'اسم الطالب',
            'participant_id': 'الرقم القومي',
            'sheikh_name': 'اسم الشيخ المحفظ',
            'phone': 'رقم الهاتف',
            'parts_count': 'عدد الأجزاء',
            'season_year': 'الموسم',
            'result': 'النتيجة',
            'rank': 'الترتيب',
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
            'season_year': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثال: 2026',
                'min': '2020',
                'max': '2100',
            }),
            'result': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'مثال: 95.50 أو ممتاز',
            }),
            'rank': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'اختياري',
                'min': '1',
            }),
        }
        help_texts = {
            'season_year': 'السنة اللي الطالب مسجّل فيها (مثال: 2025)',
            'rank': 'اتركه فارغًا إذا لم يُحدَّد ترتيب بعد',
        }

    def clean_participant_id(self):
        raw = self.cleaned_data['participant_id']
        normalized = normalize_digits(raw)

        if not normalized.isdigit():
            raise forms.ValidationError('الرقم القومي يجب أن يحتوي على أرقام فقط.')

        if len(normalized) != 14:
            raise forms.ValidationError('الرقم القومي يجب أن يكون 14 رقمًا.')

        qs = Participant.objects.filter(participant_id=normalized)
        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        # لو نفس الطالب ومسجّل في نفس الموسم → نرفض
        if qs.filter(season_year=self.cleaned_data.get('season_year')).exists():
            raise forms.ValidationError('هذا الرقم القومي مسجّل بالفعل في هذا الموسم.')

        return normalized

    def clean_phone(self):
        raw = self.cleaned_data['phone']
        normalized = normalize_digits(raw)

        if not normalized.isdigit():
            raise forms.ValidationError('رقم الهاتف يجب أن يحتوي على أرقام فقط.')

        if len(normalized) < 7 or len(normalized) > 15:
            raise forms.ValidationError('رقم الهاتف غير صحيح.')

        return normalized

    def clean_rank(self):
        rank = self.cleaned_data.get('rank')
        return rank or None


class ManageLoginForm(forms.Form):
    username = forms.CharField(
        label='اسم المستخدم',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'اسم المستخدم',
            'autocomplete': 'username',
            'autofocus': True,
        }),
    )
    password = forms.CharField(
        label='كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'كلمة المرور',
            'autocomplete': 'current-password',
        }),
    )
