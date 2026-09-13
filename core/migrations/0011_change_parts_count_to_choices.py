from django.db import migrations, models


def convert_parts_count(apps, schema_editor):
    """تحويل القيم القديمة (أرقام) للخيارات الجديدة."""
    Participant = apps.get_model('core', 'Participant')

    mapping_simple = {
        1: '1',
        2: '2',
        3: '3',
        4: '4',
        5: '5',
    }

    for p in Participant.objects.all():
        old = str(p.parts_count).strip()

        if old in ('1', '2', '3', '4', '5'):
            p.parts_count = old
        else:
            try:
                num = int(old)
                if num <= 5:
                    p.parts_count = str(num)
                elif num <= 10:
                    p.parts_count = 'quarter'
                elif num <= 20:
                    p.parts_count = 'half'
                else:
                    p.parts_count = 'full'
            except (ValueError, TypeError):
                p.parts_count = '1'
        p.save(update_fields=['parts_count'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_alter_participant_options_participant_season_year_and_more'),
    ]

    operations = [
        migrations.RunPython(convert_parts_count, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='participant',
            name='parts_count',
            field=models.CharField(
                choices=[
                    ('1', 'جزء واحد'),
                    ('2', 'جزئين'),
                    ('3', 'ثلاثة أجزاء'),
                    ('4', 'أربعة أجزاء'),
                    ('5', 'خمسة أجزاء'),
                    ('quarter', 'ربع القرآن'),
                    ('half', 'نصف القرآن'),
                    ('full', 'القرآن كاملًا'),
                ],
                max_length=20,
                verbose_name='عدد الأجزاء',
            ),
        ),
    ]
