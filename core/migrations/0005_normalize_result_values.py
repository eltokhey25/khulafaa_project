from django.db import migrations


def normalize_result_values(apps, schema_editor):
    Participant = apps.get_model('core', 'Participant')
    for participant in Participant.objects.all().iterator():
        if participant.result is not None:
            participant.result = str(participant.result).strip()
            participant.save(update_fields=['result'])


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_participant_id_alter_participant_result'),
    ]

    operations = [
        migrations.RunPython(normalize_result_values, migrations.RunPython.noop),
    ]
