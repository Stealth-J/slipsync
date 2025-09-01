import requests
import time
import httpx, asyncio
from ssync.models import Tournament
import json
import re
from types import SimpleNamespace
from datetime import datetime, timezone


class TaskError(Exception):
    pass


b9_tourney_games_url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEventsInGroupV2?GROUPID={}&DISP=0&GROUPMARKETID=1&v_cache_version=1.285.4.198'
b9_game_markets_url = 'https://sports.bet9ja.com/desktop/feapi/PalimpsestAjax/GetEvent?EVENTID={}&v_cache_version=1.285.0.198'
sporty_tourney_games_url = 'https://www.sportybet.com/api/ng/factsCenter/pcEvents'
sporty_game_markets_url = 'https://www.sportybet.com/api/ng/factsCenter/event?eventId=sr%3Amatch%3A{}&productId=3&_t={}'

sporty_payload =  [{
    "sportId": "sr:sport:1",
    "marketId": "1,18,10,29,11,26,36,14",
    "tournamentId": [[{}]]
}]

TOURNAMENT_URL_HEADERS = {
    'sportybet': {
        'Content-Type': 'application/json',
        'Origin': 'https://www.sportybet.com',
        'Referer': 'https://www.sportybet.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    },
    'bet9ja': 
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36",
            "Accept": "application/json",
            "Referer": "https://www.bet9ja.com/",  
            "Origin": "https://www.bet9ja.com",  
        },
        
}

GAME_MARKET_URL_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded",
    "Origin": "https://sports.bet9ja.com",
    "Referer": "https://sports.bet9ja.com/",
}


def get_sporty_id_digit(string):
    digit = re.sub(r'sr:match:', '', string)
    return digit


def get_current_time_formatted():
    timestamp_now = datetime.now().replace(tzinfo = timezone.utc)
    timestamp_now = int(timestamp_now.timestamp() * 1000)
    return timestamp_now


def retrieve_matches_teams_b9(matches_data):
    matches = []
    for match in matches_data:
        match_str = match['DS']
        match_id = str(match['ID'])
        home, away = match_str.split(' - ')
        matches.append((home, away, match_id ))
    
    return matches


def retrieve_matches_teams_sporty(matches_data):
    matches = []
    for match in matches_data:
        match_id = match['eventId']
        home = match['homeTeamName']
        away = match['awayTeamName']
        match_id = get_sporty_id_digit(match_id)
        matches.append((home, away, match_id ))
    
    return matches




async def check_market_validity_b9(client, selection):
    if selection.closest_match and not selection.expired:
        _, _, game_id = selection.closest_match
        if selection.tourney_ids and selection.booking_data:
            game_url = b9_game_markets_url.format(game_id)

            try:
                response = await client.get(game_url, headers = GAME_MARKET_URL_HEADERS)
                response.raise_for_status()
                market_labels = response.json()['D']['O']
                
                for k, v in market_labels.items():
                    if k == selection.booking_data:
                        selection.supported = True
                        break
                else:    
                    selection.supported = False
                    selection.market_supported = False
            except Exception as e:
                raise e
        else:
            selection.supported = False
    else:
        selection.supported = False
        
    return selection



async def check_market_validity_sporty(client, selection):
    if selection.closest_match and not selection.expired:
        _, _, game_id = selection.closest_match
        if selection.tourney_ids and selection.booking_data:
            s_market_id, s_specifier, s_pick_id = selection.booking_data

            timestamp_now = get_current_time_formatted()
            game_url = sporty_game_markets_url.format(game_id, timestamp_now)

            try:
                response = await client.get(game_url, headers = TOURNAMENT_URL_HEADERS['sportybet'])
                response.raise_for_status()
                markets_data = response.json().get("data", {}).get("markets", [])
                
                for market in markets_data:
                    market_id = market['id']
                    outcomes_ids = [ each['id'] for each in market['outcomes'] ]
                    if market_id == s_market_id:
                        if s_pick_id in outcomes_ids:
                            selection.supported = True
                            break
                        
                else:
                    selection.supported = False
                    selection.market_supported = False

            except Exception as e:
                raise e
            
        else:
            selection.supported = False

    else:
        selection.supported = False

    return selection






async def grab_tourney_games_b9(tourney_id, client):
    t_start = time.perf_counter()
    headers = TOURNAMENT_URL_HEADERS['bet9ja']
    try:
        url = b9_tourney_games_url.format(tourney_id)

        t0 = time.perf_counter()
        response = await client.get(url, headers = headers)
        print(f"[HTTP POST] {time.perf_counter() - t0:.4f}s")

        response.raise_for_status()
        data = response.json()['D']['E']
    
    except Exception as e:
        print(f"\033[1;91mError: {e}\033[0m")
        raise e

    print(f"[TOTAL per tournament] {time.perf_counter() - t_start:.4f}s")

    data_obj = SimpleNamespace(id_ = tourney_id, json_ = data)
    return data_obj


async def grab_tourney_games_and_markets_sporty(tourney_id, client):
    t_start = time.perf_counter()
    payload = sporty_payload
    payload[0]['tournamentId'] = [[ tourney_id ]]
    headers = TOURNAMENT_URL_HEADERS['sportybet']
    try:
        t0 = time.perf_counter()
        response = await client.post(sporty_tourney_games_url, headers = headers, json = payload)
        print(f"[HTTP POST] {time.perf_counter() - t0:.4f}s")

        response.raise_for_status()
        data = response.json()['data'][0]['events']

    except Exception as e:
        print(f"\033[1;91mError: {e}\033[0m")
        raise e
    
    print(f"[TOTAL per tournament] {time.perf_counter() - t_start:.4f}s\n")

    data_obj = SimpleNamespace(id_ = tourney_id, json_ = data)
    return data_obj

