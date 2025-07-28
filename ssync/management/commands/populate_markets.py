from django.core.management.base import BaseCommand
from ssync.models import Market

class Command(BaseCommand):
    help = "Populate Market model from Markets.md"

    def handle(self, *args, **options):

        with open('sites_json/testscript.txt', 'r', encoding='utf-8') as f:
            content = f.read()

        blocks = content.strip().split("\n\n")  # Split by empty lines

        for block in blocks:
            lines = block.strip().splitlines()
            if len(lines) < 3:
                continue  # Skip incomplete blocks

            name = lines[0].strip()
            b9_id = lines[1].strip()
            sporty_id = lines[2].strip()

            # Skip if sporty_id is 'none'
            if sporty_id.lower() == 'none':
                sporty_id = None

            # Also treat 'none' b9_id as null
            if b9_id.lower() == 'none':
                b9_id = None

            Market.objects.create(
                name = name,
                b9_identifier = b9_id,
                sporty_id = sporty_id
            )

        self.stdout.write(self.style.SUCCESS('Markets successfully created'))
