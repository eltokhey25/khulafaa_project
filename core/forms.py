from django import forms

from .models import Participant
from .utils import normalize_digits


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ('name', 'participant_id', 'result', 'rank')
        labels = {
            'name': 'اسم الطالب',
            'participant_id': 'الرقم القومي',
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
        if qs.exists():
            raise forms.ValidationError('هذا الرقم القومي مسجّل مسبقًا.')

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
