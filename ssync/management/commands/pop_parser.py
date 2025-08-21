from django.core.management.base import BaseCommand
from ssync.models import Market, Outcome, MarketParser
import json

class Command(BaseCommand):
    help = "Populate Market model from Markets.md"

    def handle(self, *args, **options):
        try:
            objs_created = []
            ids = [       '184'     ]
            exempt = [   ''     ]
            dict_i = 'b9_dict_first_goal_1x2'
            func_ = 'b9_parse_1x2'

            from_platform = 'sportybet'
            to_platform = 'bet9ja'
            ids = [ str(id_) for id_ in ids ]
            ids = [ id for id in ids if id not in exempt ]

            for i in ids:
                market_obj = Market.objects.filter(sporty_id = i)
                for obj in market_obj:
                    parser_obj = MarketParser(market = obj, to_platform = to_platform, from_platform = from_platform, dictionary = dict_i, parser_func = func_)
                    objs_created.append(parser_obj)

            MarketParser.objects.bulk_create(objs_created)

            print('Created successfully - ', dict_i, f'  \033[92m{len(objs_created)}\033[0m')

        except Exception as e:
            print('Error: ', e)
