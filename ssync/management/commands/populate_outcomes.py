from django.core.management.base import BaseCommand
from ssync.models import Market, Outcome
import json
import re

class Command(BaseCommand):
    help = "Populate Market model from Markets.md"

    def handle(self, *args, **options):
    
        markets_all = Market.objects.all()

        outcomes = []
        with open('sites_json/larger_market.json', 'r', encoding = "utf-8") as f:
            try:
                data = json.load(f)

                markets = data['data']['markets']
                outcomes = []
                i = 0
                for each in markets:  
                    id = each['id']
                    if id in ['160', '161']:
                        specifier = each.get('specifier')
                        if specifier:
                            identifier = specifier.replace('minute=', '')
                    
                        markets_obj = markets_all.filter(sporty_id=id).first()
                        if not markets_obj:
                            continue

                        for outcome in each.get('outcomes', []):
                            outcome_id = outcome.get('id')
                            desc = outcome.get('desc')

                            outcome_obj = Outcome(
                                market=markets_obj,
                                outcome_id=outcome_id,
                                desc=desc,
                                specifier=specifier
                            )
                            outcomes.append(outcome_obj)
                            i+=1
                            print(f'{specifier} - {desc} - {markets_obj.name} - ({outcome_id})')

                Outcome.objects.bulk_create(outcomes)
                print('Successful')
                
            except Exception as e:
                print(f'Error: {e}')
                



























































# class Command(BaseCommand):
#     help = "Populate Market model from Markets.md"

#     def handle(self, *args, **options):
    
#         markets_all = Market.objects.all()

#         outcomes = []
                
#         with open('sites_json/sporty_markets.json', 'r', encoding = "utf-8") as f:
#             try:
#                 data = json.load(f)
#                 markets = data['data']['markets']

#                 for market in markets:
#                     market_id = market.get("id")
#                     specifier = market.get("specifier")  # may be None
#                     outcomes = market.get("outcomes", [])

#                     db_markets = Market.objects.filter(sporty_id=market_id)
#                     if not db_markets:
#                         continue

#                     for db_market in db_markets:
#                         for outcome in outcomes:
#                             outcome_id = outcome.get("id")
#                             desc = outcome.get("desc")
#                             desc = desc.replace("Besiktas Istanbul", "{Home}").replace("Shakhtar D", "{Away}")

#                             db_outcome = Outcome.objects.filter(
#                                 market=db_market,
#                                 outcome_id=outcome_id,
#                                 desc=desc
#                             ).first()

#                             if db_outcome:
#                                 if specifier and db_outcome.specifier != specifier:
#                                     db_outcome.specifier = specifier
#                                     db_outcome.save(update_fields=["specifier"])
#                                     print(f"✅ Updated {db_market.name} - {desc} with specifier {specifier}")
#                             else:
#                                 print(f"⚠️ Outcome {desc} ({outcome_id}) not found for market {db_market.name}")

#             except Exception as e:
#                 print(f"❌ Error with market ")