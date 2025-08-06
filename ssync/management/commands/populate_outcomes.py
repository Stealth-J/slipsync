from django.core.management.base import BaseCommand
from ssync.models import Market, Outcome
import json

class Command(BaseCommand):
    help = "Populate Market model from Markets.md"

    def handle(self, *args, **options):
    
        markets_all = Market.objects.all()

        outcomes = []
        with open('sites_json/sporty_markets.json', 'r', encoding = "utf-8") as f:
            try:
                data = json.load(f)

                markets = data['data']['markets']
                for each in markets:
                    id = each['id']
                    markets_obj = markets_all.filter(sporty_id = id)

                    if markets_obj:
                        for market_obj in markets_obj:
                            for outcome in each.get('outcomes'):
                                outcome_id = outcome.get('id')
                                desc = outcome.get('desc')
                                outcome_obj = Outcome(market = market_obj, outcome_id = outcome_id, desc = desc)
                                outcomes.append(outcome_obj)

                Outcome.objects.bulk_create(outcomes)
                print('Successful')
                
            except Exception as e:
                print(f'Error: {e}')
                