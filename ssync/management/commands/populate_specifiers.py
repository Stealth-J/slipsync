from django.core.management.base import BaseCommand
from ssync.models import Market, Outcome
import json

class Command(BaseCommand):
    help = "Populate Market model from Markets.md"

    def handle(self, *args, **options):
        with open('sites_json/sporty_markets.json', 'r', encoding = "utf-8") as f:
            try:
                data = json.load(f)

                markets = data['data']['markets']
                for each in markets:
                    id = each['id']
                    specifier = each.get('specifier', '')

                    market_obj = Market.objects.filter(sporty_id = id)
                    
                    if specifier:
                        for one in market_obj:
                            one.specifier = specifier
                            one.save()

            except Exception as e:
                raise e