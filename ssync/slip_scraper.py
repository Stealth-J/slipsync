import requests
from datetime import datetime, timezone
from urllib.parse import urlparse
import json
from .helpers import format_time, get_timestamp
from types import SimpleNamespace
from .context_processors import *
from .helpers import parse_overs_and_unders


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
    print(url)
    headers = HEADERS.get(platform)
    if not headers:
        return (False, f"Unknown platform '{platform}'")
    
    success, text = validate_url(url, platform)
    if not success:
        return (success, text)
    
    try:
        response = requests.get(url, headers = headers)
        print("Fetch time:", response.elapsed.total_seconds())

        response.raise_for_status()
        return (True, response.json())

    except Exception as e:
        return (False, f'Failed to fetch slip data: {str(e)}')

def parse_sporty(data):
    selections = []

    for outcome in data.get("data", {}).get("outcomes", []):
        try:

            home = outcome.get("homeTeamName")
            away = outcome.get("awayTeamName")
            tournament = outcome.get("sport", {}).get("category", {}).get("tournament", {}).get("name")
            start_time_ms = outcome.get("estimateStartTime")
            start_time = format_time(start_time_ms)
            
            status = outcome.get("matchStatus", 'none')
            status_class = game_status.get(status.lower(), 'unknown')

            market_data = outcome.get("markets", [])[0] if outcome.get("markets") else {}
            market = market_data.get("desc")
            pick_data = market_data.get("outcomes", [])[0] if market_data.get("outcomes") else {}
            pick = pick_data.get("desc")
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
        
        selections.append(SimpleNamespace(home_team = home, away_team = away, league = tournament, start_time = start_time, status = status, market_type = market, pick = pick, odds = odds, error = error, status_class = status_class))

    return selections

def parse_b9(data):
    selections = []

    events = data.get("D", {}).get("O", {})
    trans = data.get("D", {}).get("TRANS", {})
# 37N9JTV 
    for key, val in events.items():
        game_id, rest = key.split('$S_')
        print(key)
        
        e_name = val.get("E_NAME", "")
        home, away = e_name.split(" - ") if " - " in e_name else (e_name, None)

        tournament = val.get("GN")
        start_time_ms = val.get("STARTDATE")
        start_time = format_time(get_timestamp('Bet9ja', start_time_ms))

        status = "Unknown"
        status_class = game_status.get(status.lower(), 'unknown')

        market = val.get("M_NAME")
        pick = val.get('SGN', '')
        pick = parse_overs_and_unders(pick, rest)

        odds = val.get("V", 0)

        try:
            odds = float(odds)
            error = ''
        except Exception as e:
            odds = 0
            error = str(e)

        selections.append(SimpleNamespace(home_team = home, away_team = away, league = tournament, start_time = start_time, status = status, market_type = market, pick = pick, odds = odds, error = error, status_class = status_class))

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