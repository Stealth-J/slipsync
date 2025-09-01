from .models import *
from celery import shared_task
import requests
import logging
from .helpers import get_current_time_formatted, get_tourney_obj

logger = logging.getLogger(__name__)

URLS = {
    'bet9ja': 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetSports?DISP=0&v_cache_version=1.287.0.198',
    'sportybet': 'https://www.sportybet.com/api/ng/factsCenter/popularAndSportList?sportId=sr%3Asport%3A{}&_t={}'
}
HEADERS = { "User-Agent": "Mozilla/5.0" }

@shared_task
def find_new_tournaments_b9():
    all_ids = list(Tournament.objects.exclude(b9_id = None).values_list('b9_id', flat = True))
    already_registered_ids = list(NotSupportedTournament.objects.filter(market_platform = 'bet9ja').values_list('identifier', flat = True))
    tourneys_all = list(Tournament.objects.all())

    try:
        url = URLS['bet9ja']
        response = requests.get(url, headers = HEADERS, timeout = 40)
        new_ = []
        updated_ = []
        data = response.json()['D']['PAL']['1']
        for _, each in data['SG'].items():
            c_desc = each['SG_LANG']['en']
            for key, each_ in each['G'].items():
                desc = each_['G_DESC']
                if key not in all_ids and key not in already_registered_ids:
                    if key not in already_registered_ids:
                        bool_, obj = get_tourney_obj(tourneys_all, (c_desc, desc), 'b9_name')
                        if bool_:
                            obj.b9_id = key
                            updated_.append(obj)
                            print(f'[{c_desc}] || {desc} - ({key}) --- UPDATED')
                        else:
                            new_.append(NotSupportedTournament(country = c_desc, identifier = key, market_platform = 'bet9ja', tourney_name = desc))
                            print(f'[{c_desc}] || {desc} - ({key})')

        NotSupportedTournament.objects.bulk_create(new_)
        Tournament.objects.bulk_update(updated_, ['b9_id'])

    except requests.exceptions.RequestException as e:
        logger.error(f"Network related error: {e}")
    except Exception as e:
        logger.error(f"Error: {type(e).__name__} - {e}")
        Error.objects.create(error_type = type(e).__name__, error_message = f'{url}: {str(e)}')



@shared_task
def find_new_tournaments_sporty():
    all_ids = list(Tournament.objects.exclude(sporty_id = None).values_list('sporty_id', flat = True))
    already_registered_ids = list(NotSupportedTournament.objects.filter(market_platform = 'sportybet').values_list('identifier', flat = True))
    tourneys_all = list(Tournament.objects.all())

    try:
        url = URLS['sportybet'].format(1, get_current_time_formatted())
        response = requests.get(url, headers = HEADERS, timeout = 40)
        new_ = []
        updated_ = []
        data = response.json()['data']['sportList'][0]
        for each in data['categories']:
            c_desc = each['name']
            for each_ in each['tournaments']:
                key, desc = each_['id'], each_['name']
                if key not in all_ids:
                    if key not in already_registered_ids:
                        bool_, obj = get_tourney_obj(tourneys_all, (c_desc, desc), 'sporty_name')
                        if bool_:
                            obj.sporty_id = key
                            updated_.append(obj)
                            print(f'[{c_desc}] || {desc} - ({key}) --- UPDATED')
                        else:
                            new_.append(NotSupportedTournament(country = c_desc, identifier = key, market_platform = 'sportybet', tourney_name = desc))
                            print(f'[{c_desc}] || {desc} - ({key})')

        NotSupportedTournament.objects.bulk_create(new_)
        Tournament.objects.bulk_update(updated_, ['sporty_id'])

    except requests.exceptions.RequestException as e:
        logger.error(f"Network related error: {e}")
    except Exception as e:
        logger.error(f"Error: {type(e).__name__} - {e}")
        Error.objects.create(error_type = type(e).__name__, error_message = f'{url}: {str(e)}')



@shared_task
def find_new_tournaments():
    find_new_tournaments_b9.delay()
    find_new_tournaments_sporty.delay()
    print('Done all done')