from datetime import datetime, timezone
from functools import wraps
import time
import re
import difflib
from string import punctuation
from .context_processors import *
from .scrape_games import *
from .booking import book_b9, book_sporty

sites_urls = {
    'bet9ja': "https://coupon.bet9ja.com/desktop/feapi/CouponAjax/GetBookABetCoupon?couponCode={}&v_cache_version=1.279.0.198",
    'sportybet': "https://www.sportybet.com/api/ng/orders/share/{}?_t={}"
}

tournament_attrs = {
    'bet9ja': 'b9_id',
    'sportybet': 'sporty_id'
}

dict_tournament_funcs = {
    'bet9ja': grab_tourney_games_b9,
    'sportybet': grab_tourney_games_and_markets_sporty
}

dict_retrieve_matches_funcs = {
    'bet9ja': retrieve_matches_teams_b9,
    'sportybet': retrieve_matches_teams_sporty,
}

dict_check_market_validity = {
    'bet9ja': check_market_validity_b9,
    'sportybet': check_market_validity_sporty,
}

dict_booking = {
    'bet9ja': book_b9,
    'sportybet': book_sporty,
}


def timeit(label = None):    # so we can put arguments in the decorator
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            duration = time.time() - start
            tag = label or func.__name__
            print(f"[{tag}] took {duration:.2f} seconds")

            return result
        return wrapper
    return decorator


def format_time(time_data, ms = True):
    ms_time = time_data
    if ms:
        ms_time = datetime.fromtimestamp(time_data / 1000, tz = timezone.utc)
    
    time = ms_time.strftime("%I:%M %p · %B %d, %Y")
    return time[1:] if time.startswith('0') else time


def check_game_expiry(string):
    dt = datetime.strptime(string, "%I:%M %p · %B %d, %Y")
    dt = dt.replace(tzinfo = timezone.utc)
    dt_now = datetime.now().replace(tzinfo = timezone.utc)
    return int(dt.timestamp() * 1000) < int(dt_now.timestamp() * 1000)


def get_url(slip_code, platform):
    try:
        url_raw = sites_urls.get(platform, None)
        timestamp = get_timestamp(platform)

        url = url_raw.format(slip_code, timestamp)

        return url
    
    except Exception as e:
        return

def get_timestamp(platform, time_raw = None):
    if platform == 'sportybet':
        dt = datetime.now()

    elif platform == 'bet9ja':
        if time_raw == None:
            return None

        dt = datetime.strptime(time_raw, "%Y-%m-%d %H:%M:%S")
    
    else:
        return 
    
    timestamp = int(dt.timestamp() * 1000)

    return timestamp


def return_next_platform(platform):
    formatted_list = [ site for site in SUPPORTED_SITES if site != platform ]
    return formatted_list[0], formatted_list


def clean_b9_key(key):
    key = key.removeprefix('M#').removesuffix('.NAME')
    return key


def clean_b9_pick(string, b9_prefix):
    return string.replace(b9_prefix, '')


def prepare_for_parsing(pick, market_obj, teams):
    home, away = teams
    if market_obj.sporty_id in ['819', '820']:
        pick = pick.replace(home, '{Home}').replace(away, '{Away}')

    
    return pick


def parse_game_b9_fields(key, val, status):
    if '$LIVES_' in key:
        status = 'live'

    elif '$S_' not in key:
        return

    _, rest = key.split('$')
    e_name = val.get("E_NAME", "")
    home, away = e_name.split(" - ")
    teams = (home, away)
    tournament = val.get("GN")
    start_time_ms = val.get("STARTDATE")
    start_time = format_time(get_timestamp('bet9ja', start_time_ms))
    status_class = game_status.get(status.lower(), 'unknown')
    market_desc = val.get("M_NAME")
    pick = val.get('SGN', '')
    odds = val.get("V", 0)  if status == 'Unknown' else '-'
    market_id = clean_b9_key(val.get('marketNameTransKey'))
    tourney_id = str(val.get('GID'))

    game_fields = {
        'rest': rest,
        'home': home,
        'away': away,
        'teams': (home, away),
        'tournament': tournament,
        'start_time': start_time,
        'status': status,
        'market_desc': market_desc,
        'pick': pick,
        'odds': odds,
        'status_class': status_class,
        'market_id': market_id,
        'tourney_id': tourney_id,
    }

    return game_fields



def parse_game_sporty_fields(outcome):
    sport = outcome.get('sport').get('id')
    if sport != 'sr:sport:1':
        return

    home = outcome.get("homeTeamName")
    away = outcome.get("awayTeamName")
    teams = (home, away)
    tournament = outcome.get("sport", {}).get("category", {}).get("tournament", {}).get("name")
    start_time_ms = outcome.get("estimateStartTime")
    start_time = format_time(start_time_ms)
    status = outcome.get("matchStatus", 'none')
    status_class = game_status.get(status.lower(), 'unknown')
    market_data = outcome.get("markets")
    market_data = market_data[0] if market_data else {}
    market_desc = market_data.get("desc")
    pick_data = market_data.get("outcomes")
    pick_data = pick_data[0] if pick_data else {}
    pick = pick_data.get("desc")
    odds = pick_data.get("odds") if not outcome.get('setScore') else '-'
    market_id =  market_data.get('id')
    tourney_id = outcome.get("sport").get("category").get("tournament").get("id")

    game_fields = {
        'home_team': home, 
        'away_team': away, 
        'teams': teams,
        'league': tournament, 
        'start_time': start_time, 
        'status': status, 
        'market_type': market_desc, 
        'pick': pick, 
        'odds': odds, 
        'status_class': status_class, 
        'market_id': market_id,
        'tourney_id': tourney_id
    }

    return game_fields



def platforms_are_supported(platforms):
    not_permitted = ['nairabet', 'betking']

    for platform_ in platforms:
        if platform_.lower() in not_permitted:
            return False, f'{platform_} is not supported right now. Work in progress'

    return True, ''


def filter_parser_data(obj, from_, to_):
    parser_objs = []
    for i in obj.parser_data.all():
        if i.from_platform.lower() == from_.lower() and i.to_platform.lower() == to_.lower():
            parser_objs.append(i)

    if parser_objs:
        return parser_objs[0]
    
    return parser_objs


def get_market_object(market_field, markets_all, market_id):
    market_obj = None

    for obj in markets_all:
        if getattr(obj, market_field) == market_id:
            market_obj = obj
            break

    return market_obj


def get_tourney_objects(tourney_field, tourneys_all, tourney_id):
    tourney_objs = []

    for obj in tourneys_all:
        if getattr(obj, tourney_field) == tourney_id:
            tourney_objs.append(obj)
    
    return tourney_objs


def create_booking_format(market_obj, pick_txt, teams, platforms):
    from_, to_ = platforms
    pick_txt = prepare_for_parsing(pick_txt, market_obj, teams)

    parser_obj = filter_parser_data(market_obj, from_, to_)

    if parser_obj:
        func_, dict_ = parser_obj.get_parser(), parser_obj.get_dict()
        if callable(func_):
            booking_data = func_(pick_txt, market_obj, dict_)
        else:
            raise Exception(f'{parser_obj} cannot be called')
        
    else:
        booking_data = None
        print(f'No parsing function developed for {market_obj.name}')

    return booking_data


def filter_exceptions_out(results):
    valid_results = []

    for result in results:
        if isinstance(result, Exception):
            print(f"\033[1;91mError in task: {result}\033[0m")

        elif result:
            valid_results.append(result)

    return valid_results


def combine_tourney_json(lookup, tourney_ids):
    combined_json = [ lookup.get(id_) for id_ in tourney_ids if id_ in lookup ]
    return combined_json



def clean_team_name(name):
    name = name.replace('-', ' ').lower()
    punctuation_ = punctuation.replace('-', '')
    name = re.sub(f"[{re.escape(punctuation_)}]", "", name)
    name = re.sub(r'\s+', ' ', name)
    tokens = [t for t in name.split() if len(t) > 2]
    return tokens


def find_matching_game(teams, matches_list):
    home, away = teams
    home_tokens = clean_team_name(home)
    away_tokens = clean_team_name(away)

    suspected_match = None
    best_score = 0

    for match_home, match_away, match_id in matches_list:
        mh_tokens = clean_team_name(match_home)
        ma_tokens = clean_team_name(match_away)

        if home_tokens == mh_tokens and away_tokens == ma_tokens:
            return True, (match_home, match_away, match_id)

        if home_tokens == mh_tokens and set(away_tokens) & set(ma_tokens):
            return True, (match_home, match_away, match_id)

        if away_tokens == ma_tokens and set(home_tokens) & set(mh_tokens):
            return True, (match_home, match_away, match_id)

        if set(home_tokens) & set(mh_tokens) and set(away_tokens) & set(ma_tokens):
            return True, (match_home, match_away, match_id)
        
        if set(home_tokens) & set(mh_tokens):
            matching_ratio = difflib.SequenceMatcher(None, away, match_away).ratio()
            if matching_ratio >= 0.4:
                return True, (match_home, match_away, match_id)
            
        if set(away_tokens) & set(ma_tokens):
            matching_ratio = difflib.SequenceMatcher(None, home, match_home).ratio()
            if matching_ratio >= 0.4:
                return True, (match_home, match_away, match_id)


        combined1 = " ".join(home_tokens + away_tokens)
        combined2 = " ".join(mh_tokens + ma_tokens)
        score = difflib.SequenceMatcher(None, combined1, combined2).ratio()

        if score > best_score and score > 0.35:
            best_score = score
            suspected_match = (match_home, match_away, match_id)

    return False, suspected_match


def filter_game_slip_final(slip_data, ids_list):
    valid_games = []

    for game in slip_data:
        if game['supported'] == True:
            if game['id_'] in ids_list:
                _, _, game_id = game['closest_match']
                game['game_id'] = game_id
                valid_games.append(game)

    if len(valid_games) > 0:
        return valid_games, valid_games[0]['converted_to']
    
    raise Exception('No valid selections')