from django.db import models


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
