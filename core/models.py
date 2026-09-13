from django.db import models
from django.utils import timezone


class Participant(models.Model):
    participant_id = models.CharField(
        'الرقم القومي',
        max_length=14,
        unique=True,
        db_index=True,
    )
    name = models.CharField('الاسم', max_length=200)
    sheikh_name = models.CharField('اسم الشيخ المحفظ', max_length=200)
    phone = models.CharField('رقم الهاتف', max_length=15)
    parts_count = models.PositiveIntegerField(
        'عدد الأجزاء',
        choices=[(i, f'{i} جزء') for i in range(1, 31)],
    )
    registration_number = models.CharField(
        'رقم الاستمارة',
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )
    rank = models.PositiveIntegerField('الترتيب', null=True, blank=True)
    result = models.CharField(
        'النتيجة',
        max_length=50,
        blank=True,
        default='',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'مشارك'
        verbose_name_plural = 'المشاركون'
        ordering = [models.F('rank').asc(nulls_last=True), 'participant_id']

    def __str__(self):
        return f'{self.name} ({self.participant_id})'

    def save(self, *args, **kwargs):
        # توليد رقم الاستمارة تلقائيًا
        if not self.registration_number:
            year = timezone.now().year
            last = Participant.objects.filter(
                registration_number__startswith=f'KH-{year}-'
            ).order_by('-registration_number').first()
            if last and last.registration_number:
                try:
                    last_num = int(last.registration_number.split('-')[-1])
                except (ValueError, IndexError):
                    last_num = 0
            else:
                last_num = 0
            self.registration_number = f'KH-{year}-{last_num + 1:04d}'
        super().save(*args, **kwargs)
