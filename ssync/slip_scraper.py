import requests
from datetime import datetime, timezone
from .models import *
from urllib.parse import urlparse
import json
from .async_helpers import *
from .scrape_games import *
from asgiref.sync import async_to_sync


SLIP_DOMAINS = {
    "sportybet": ["sportybet.com", "sporty.com", "sporty.ng", "www.sportybet.com", "www.sporty.com", "www.sporty.ng"],
    "bet9ja": ["www.bet9ja.com", "www.shop.bet9ja.com", "www.coupon.bet9ja.com", "bet9ja.com", "shop.bet9ja.com", "coupon.bet9ja.com"],
    "betking": ["www.betking.com", "www.betking.ng", "betking.com", "betking.ng"],
    "nairabet": ["www.nairabet.com", "www.nairabet.ng", "nairabet.com", "nairabet.ng"],
}

HEADERS = {
    'sportybet': {
        'Content-Type': 'application/json', 
        'User-Agent': 'Mozilla/5.0', 
        'Origin': 'https://www.sportybet.com'
    },
    'bet9ja': 
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.bet9ja.com/",  # or sportybet.com if needed
            "Origin": "https://www.bet9ja.com",   # match the site
        },
        
}


def validate_url(url, platform):
    expected_domains = SLIP_DOMAINS.get(platform)
    
    if not expected_domains:
        return (False, f"Unknown platform '{platform}' ")

    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return (False, f'URL is not valid. {url}')
    
    except Exception:
        return (False, 'Malformed URL')
    
    domain = parsed.netloc.lower()
    if domain not in expected_domains:
        return (False, f"Not a valid {platform} slip ")

    return (True, '')


async def scrape_site(url, platform, client):
    headers = HEADERS.get(platform)
    if not headers:
        return (False, f"Unknown platform '{platform}'")
    
    success, text = validate_url(url, platform)
    if not success:
        return (success, text)
    
    try:
        response = await client.get(url, headers = headers)
        print("Fetch time:", response.elapsed.total_seconds())

        response.raise_for_status()
        return (True, response.json())

    except Exception as e:
        return (False, f'Failed to fetch slip data: {str(e)}')







def validate_and_get_teams():
    pass




async def parse_sporty(data, platforms, objs, client):
    outcomes = data.get("data", {}).get("outcomes", [])
    _, to_ = platforms
    grab_tournament_json_func = dict_tournament_funcs.get(to_)
    retrieve_matches_func = dict_retrieve_matches_funcs.get(to_)
    check_market_validity_func = dict_check_market_validity.get(to_)

    results = [ parse_and_scrape_sporty(id_, objs, outcome, platforms) for id_, outcome in enumerate(outcomes) ]
    selections = filter_exceptions_out(results)

    tourney_ids_all = set([ tourney_id for result in selections if result.tourney_ids for tourney_id in result.tourney_ids ])

    scrape_tasks = [ grab_tournament_json_func(tourney_id, client) for tourney_id in tourney_ids_all ]
    tourney_json_objs = await asyncio.gather(*scrape_tasks, return_exceptions = True)
    tourney_json_objs = filter_exceptions_out(tourney_json_objs)

    # with open('sites_json/b9_league.json', 'w', encoding = 'utf-8') as f:
    #     json.dump(tourney_json_objs, f, indent = 4, ensure_ascii = False)

    tourney_json_lookup = { obj.id_:obj.json_ for obj in tourney_json_objs }
    selection_json_all = [(result, combine_tourney_json(tourney_json_lookup, result.tourney_ids)) for result in selections ]

    for selection_json in selection_json_all:
        selection, json_data = selection_json
        matches_list = []
        for each in json_data:
            matches = retrieve_matches_func(each)
            for match_ in matches:
                matches_list.append(match_)

        exact, match_data = find_matching_game(selection.teams, matches_list)
        selection.exact = exact
        selection.closest_match = match_data

    scrape_markets_tasks = [ check_market_validity_func(client, selection) for selection, _ in selection_json_all ]
    final_selections = await asyncio.gather(*scrape_markets_tasks, return_exceptions = True)
    final_selections = filter_exceptions_out(final_selections)
    final_selections = sorted(final_selections, key = lambda x: x.supported, reverse = True)
    
    return final_selections



async def parse_b9(data, platforms, objs, client):
    events = data.get("D", {}).get("O", {})
    _, to_ = platforms
    grab_tournament_json_func = dict_tournament_funcs.get(to_)
    retrieve_matches_func = dict_retrieve_matches_funcs.get(to_)
    check_market_validity_func = dict_check_market_validity.get(to_)

    results = [ parse_and_scrape_b9(id_, objs, items, platforms) for id_, items in enumerate(events.items()) ]
    selections = filter_exceptions_out(results)

    tourney_ids_all = set([ tourney_id for result in selections if result.tourney_ids for tourney_id in result.tourney_ids ])

    scrape_tasks = [ grab_tournament_json_func(tourney_id, client) for tourney_id in tourney_ids_all ]
    tourney_json_objs = await asyncio.gather(*scrape_tasks, return_exceptions =  True)
    tourney_json_objs = filter_exceptions_out(tourney_json_objs)

    # with open('sites_json/b9_league2.json', 'w', encoding = 'utf-8') as f:
    #     json.dump(tourney_json_objs, f, indent = 4, ensure_ascii = False)

    tourney_json_lookup = { obj.id_: obj.json_ for obj in tourney_json_objs }
    selection_json_all = [(result, combine_tourney_json(tourney_json_lookup, result.tourney_ids)) for result in selections ]

    for selection_json in selection_json_all:
        selection, json_data = selection_json
        matches_list = []
        for each in json_data:
            matches = retrieve_matches_func(each)
            for match_ in matches:
                matches_list.append(match_)

        exact, match_data = find_matching_game(selection.teams, matches_list)
        selection.exact = exact
        selection.closest_match = match_data

    scrape_markets_tasks = [ check_market_validity_func(client, selection) for selection, _ in selection_json_all ]
    final_selections = await asyncio.gather(*scrape_markets_tasks, return_exceptions = True)
    final_selections = filter_exceptions_out(final_selections)
    final_selections = sorted(final_selections, key = lambda x: x.supported, reverse = True)

    return final_selections


parse_functions = {
    'sportybet': parse_sporty,
    'bet9ja': parse_b9
}


async def parse_slip(url, platforms, objs):
    from_, to_ = platforms
    permitted, error_txt = platforms_are_supported(platforms)
    selections = []
    
    async with httpx.AsyncClient(timeout = 50) as client:
        success, data = await scrape_site(url, from_, client)
        if not success:
            return (False, data)

        func = parse_functions.get(from_, '')
        if callable(func) and permitted:
            selections = await func(data, platforms, objs, client)

    if not selections:
        error_txt = error_txt or 'Failed to parse slip data. Check if the right platform is chosen'     # give a list of options of what possibly happened
        return (False, error_txt)

    return (True, selections) 



#  RK9PE4   QBNY0N  L1ESLG  JJMUM7  XCCYD7  K3U01W  QTM2U0
# 3B2JVWS  3B2RPBV  3BK86TD  3BK8SPJ    3BSKBPL

# ('1', '3')
# market_id, specifier, pick_id
# 'S_1X21_11'