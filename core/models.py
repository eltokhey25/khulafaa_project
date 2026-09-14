from django.db import models
from django.utils import timezone


class Participant(models.Model):
    PARTS_CHOICES = [
        ('1', 'جزء واحد'),
        ('2', 'جزئين'),
        ('3', 'ثلاثة أجزاء'),
        ('4', 'أربعة أجزاء'),
        ('5', 'خمسة أجزاء'),
        ('quarter', 'ربع القرآن'),
        ('half', 'نصف القرآن'),
        ('full', 'القرآن كاملًا'),
    ]

    participant_id = models.CharField(
        'الرقم القومي',
        max_length=14,
        db_index=True,
    )
    name = models.CharField('الاسم', max_length=200)
    sheikh_name = models.CharField('اسم الشيخ المحفظ', max_length=200)
    phone = models.CharField('رقم الهاتف', max_length=15)
    parts_count = models.CharField(
        'عدد الأجزاء',
        max_length=20,
        choices=PARTS_CHOICES,
    )
    registration_number = models.CharField(
        'رقم الاستمارة',
        max_length=20,
        unique=True,
        blank=True,
        null=True,
        db_index=True,
    )
    season_year = models.PositiveIntegerField(
        'سنة التسجيل',
        default=timezone.now().year,
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
        ordering = ['-season_year', models.F('rank').asc(nulls_last=True), 'participant_id']
        constraints = [
            models.UniqueConstraint(
                fields=['participant_id', 'season_year'],
                name='unique_participant_per_season',
            ),
        ]

    def __str__(self):
        return f'{self.name} ({self.participant_id}) - {self.season_year}'

    def save(self, *args, **kwargs):
        # توليد رقم الاستمارة تلقائيًا
        if not self.registration_number:
            year = self.season_year or timezone.now().year
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

        if not self.season_year:
            self.season_year = timezone.now().year

        super().save(*args, **kwargs)

    @property
    def parts_label(self):
        return dict(self.PARTS_CHOICES).get(self.parts_count, '')

    @property
    def result_display(self):
        """عرض النتيجة بصيغة '40/50'."""
        if not self.result:
            return '—'
        return f'{self.result}/50'
