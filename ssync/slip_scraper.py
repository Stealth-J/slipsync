import requests
from datetime import datetime, timezone
from .models import *
from urllib.parse import urlparse
import json
from .helpers import *
from types import SimpleNamespace
from .context_processors import *
from .market_parser import parse_1x2


SLIP_DOMAINS = {
    "SportyBet": ["sportybet.com", "sporty.com", "sporty.ng", "www.sportybet.com", "www.sporty.com", "www.sporty.ng"],
    "Bet9ja": ["www.bet9ja.com", "www.shop.bet9ja.com", "www.coupon.bet9ja.com", "bet9ja.com", "shop.bet9ja.com", "coupon.bet9ja.com"],
    "BetKing": ["www.betking.com", "www.betking.ng", "betking.com", "betking.ng"],
    "NairaBet": ["www.nairabet.com", "www.nairabet.ng", "nairabet.com", "nairabet.ng"],
}

HEADERS = {
    'SportyBet': {'Content-Type': 'application/json', 'User-Agent': 'Mozilla/5.0', 'Origin': 'https://www.sportybet.com'},
    'Bet9ja': 
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
        return (False, f"Unknown platform '{platform}'")

    try:
        parsed = urlparse(url)
        if not all([parsed.scheme, parsed.netloc]):
            return (False, 'URL is not valid.')
    
    except Exception:
        return (False, 'Malformed URL')
    
    domain = parsed.netloc.lower()
    if domain not in expected_domains:
        return (False, f"Not a valid {platform} slip ")

    return (True, '')


def scrape_site(url, platform):
    headers = HEADERS.get(platform)
    if not headers:
        return (False, f"Unknown platform '{platform}'")
    
    success, text = validate_url(url, platform)
    if not success:
        return (success, text)
    
    try:
        response = requests.get(url, headers = headers, timeout = 15)
        print("Fetch time:", response.elapsed.total_seconds())

        response.raise_for_status()
        return (True, response.json())

    except Exception as e:
        return (False, f'Failed to fetch slip data: {str(e)}')


@timeit(label='Parsing and identifying sporty markets')
def parse_sporty(data):
    selections = []
    markets_all = list(Market.objects.all())

    for outcome in data.get("data", {}).get("outcomes", []):
        try:
            market_obj = None

            home = outcome.get("homeTeamName")
            away = outcome.get("awayTeamName")
            tournament = outcome.get("sport", {}).get("category", {}).get("tournament", {}).get("name")
            start_time_ms = outcome.get("estimateStartTime")
            start_time = format_time(start_time_ms)
            
            status = outcome.get("matchStatus", 'none')
            status_class = game_status.get(status.lower(), 'unknown')

            market_data = outcome.get("markets")
            market_data = market_data[0] if market_data else {}
            market = market_data.get("desc")
            
            market_id =  market_data.get('id', '')
            for obj in markets_all:
                if obj.sporty_id == market_id:
                    market_obj = obj
                    break
                
            if market_obj:
                print(market_obj.name)
                supported =  True
            else:
                print('Not supported', market)
                supported = False
                continue

            pick_data = market_data.get("outcomes")
            pick_data = pick_data[0] if pick_data else {}
            pick = pick_data.get("desc")
            pick = pick.lower()
            odds = pick_data.get("odds" )

            try:
                odds = float(odds)
                error = ''
            except Exception as e:
                odds = 0
                error = str(e)

        except Exception as e:
            print(str(e))
            continue
        
        selections.append(SimpleNamespace(home_team = home, away_team = away, league = tournament, start_time = start_time, status = status, market_type = market, pick = pick, odds = odds, error = error, status_class = status_class, supported = supported))

    return selections

@timeit(label='Parsing and identifying bet9ja markets')
def parse_b9(data):
    markets_all = list(Market.objects.all())
    selections = []

    events = data.get("D", {}).get("O", {})
    trans = data.get("D", {}).get("TRANS", {})
 
    for key, val in events.items():
        # Ensure only "$S_"
        if '$S_' not in key:
            continue

        market_obj = None
        game_id, rest = key.split('$')
        print(key, val)
        
        e_name = val.get("E_NAME", "")
        home, away = e_name.split(" - ") if " - " in e_name else (e_name, None)

        tournament = val.get("GN")
        start_time_ms = val.get("STARTDATE")
        start_time = format_time(get_timestamp('Bet9ja', start_time_ms))

        status = "Unknown"
        status_class = game_status.get(status.lower(), 'unknown')

        market = val.get("M_NAME")
        pick = val.get('SGN', '')

        market_key = val.get('marketNameTransKey')
        market_id = clean_b9_key(market_key)
        for obj in markets_all:
            if obj.b9_id:
                if obj.b9_id == market_id:
                    market_obj = obj
                    break

        if market_obj:
            pick_txt = clean_b9_pick(rest, market_obj.b9_prefix)
            parser_obj = market_obj.parser_data.all().first()
            if parser_obj:
                func_, dict_ = parser_obj.get_parser(), parser_obj.get_dict()

                if callable(func_):
                    sporty_equ = func_('bet9ja', pick_txt, market_obj, dict_)

            else:
                sporty_equ = ''
                print(f'No parsing function developed')

            print(sporty_equ)
            # print(rest)
            supported = True
        else:
            print('Not supported:', market)
            supported = False
            continue

        odds = val.get("V", 0)

        try:
            odds = float(odds)
            error = ''
        except Exception as e:
            odds = 0
            error = str(e)

        selections.append(SimpleNamespace(home_team = home, away_team = away, league = tournament, start_time = start_time, status = status, market_type = market, pick = pick, odds = odds, error = error, status_class = status_class, supported = supported))

    return selections


parse_functions = {
    'SportyBet': parse_sporty,
    'Bet9ja': parse_b9
}

def parse_slip(url, platform):
    success, data = scrape_site(url, platform)

    if not success:
        return (False, data)
    
    selections = []

    func = parse_functions.get(platform, '')
    if callable(func):
        selections = func(data)

    if not selections:
        return (False, f'Failed to parse slip data. Check if the right platform is chosen')

    return (True, selections) 