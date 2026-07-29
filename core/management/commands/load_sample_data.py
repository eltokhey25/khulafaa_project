from django.core.management.base import BaseCommand

from core.models import Participant


SAMPLE_DATA = [
    {
        'participant_id': '29501011234567',
        'name': 'أحمد محمد العلي',
        'rank': 1,
        'result': '98.50',
    },
    {
        'participant_id': '29802022345678',
        'name': 'فاطمة حسن المحمد',
        'rank': 2,
        'result': '96.75',
    },
    {
        'participant_id': '30103033456789',
        'name': 'عمر عبدالله السعد',
        'rank': 3,
        'result': '95.00',
    },
    {
        'participant_id': '30404044567890',
        'name': 'مريم إبراهيم الخالد',
        'rank': 4,
        'result': '92.25',
    },
    {
        'participant_id': '30705055678901',
        'name': 'يوسف سالم النور',
        'rank': 5,
        'result': '90.00',
    },
]


class Command(BaseCommand):
    help = 'Load sample participant data for testing'

    def handle(self, *args, **options):
        created = 0
        for entry in SAMPLE_DATA:
            _, was_created = Participant.objects.update_or_create(
                participant_id=entry['participant_id'],
                defaults={
                    'name': entry['name'],
                    'rank': entry['rank'],
                    'result': entry['result'],
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f'Done: {created} created, {len(SAMPLE_DATA) - created} updated.')
        )
