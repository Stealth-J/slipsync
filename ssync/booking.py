import json
import copy
import requests

def multiple_selections(game_ids):
    return len(set(game_ids)) != len(game_ids)



BOOKING_URLS = {
    'bet9ja': "https://apigw.bet9ja.com/sportsbook/placebet/BookABetV2?source=desktop&v_cache_version=1.285.0.198",
    'sportybet': 'https://www.sportybet.com/api/ng/orders/share'
}

BOOKING_HEADERS = {
    'bet9ja': {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/115 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sports.bet9ja.com",
        "Referer": "https://sports.bet9ja.com/",
    },
    'sportybet': {
        "User-Agent": "Mozilla/5.0",
        "Content-Type": "application/json",
        "Origin": "https://www.sportybet.com",
        "Referer": "https://www.sportybet.com/",
    }
}


b9_payload_raw = {
    "BETSLIP": {
        "BETS": [{
            "BSTYPE": {}, 
            "TAB": {},   
            "NUMLINES": 0,   
            "COMB": 1,       
            "TYPE": 2,
            "STAKE": 0,      
            "POTWINMIN": 0,   
            "POTWINMAX": 0,   
            "BONUSMIN": 0,   
            "BONUSMAX": 0,   
            "ODDMIN": 0, 
            "ODDMAX": 0,  
            "ODDS": {},
            "FIXED": {}
        }],

        "EVS": {},
        "IMPERSONIZE": 0
    },
    "IS_PASSBET": "0"
}

def prepare_b9_payload(valid_games):
    game_ids = [ game['game_id'] for game in valid_games ]
    bstype = 2 if multiple_selections(game_ids) else 0
    form_data = copy.deepcopy(b9_payload_raw)

    form_data['BETSLIP']['BETS'][0]['BSTYPE'] = bstype
    form_data['BETSLIP']['BETS'][0]['TAB'] = bstype

    odds = [ '$'.join((game['game_id'], game['booking_data'])) for game in valid_games ]
    for odd_ in odds:
        form_data['BETSLIP']['BETS'][0]['ODDS'][odd_] = ""
    
    payload = {
        "BETSLIP": json.dumps(form_data["BETSLIP"]),
        "IS_PASSBET": form_data["IS_PASSBET"]
    }
    return payload
    

def book_b9(valid_games):
    try:
        payload = prepare_b9_payload(valid_games)
        response = requests.post(BOOKING_URLS['bet9ja'], data = payload, headers = BOOKING_HEADERS['bet9ja'], timeout = 25)
        response.raise_for_status()
        data = response.json()

        booking_code = data["data"][0].get("RIS")

    except Exception as e:
        return (False, e)

    return (True, booking_code)


sporty_payload_raw = {
    "selections": []
}

def prepare_sporty_payload(valid_games):
    payload = copy.deepcopy(sporty_payload_raw)

    for game in valid_games:
        market_id, specifier, pick_id = game['booking_data']
        game_id = f'sr:match:{game['game_id']}'
        payload["selections"].append(
            { "eventId": game_id, "marketId": market_id, "specifier": specifier, "outcomeId": pick_id }
        )
    
    return payload


def book_sporty(valid_games):
    try:
        payload = prepare_sporty_payload(valid_games)
        response = requests.post(BOOKING_URLS['sportybet'], json = payload, headers = BOOKING_HEADERS["sportybet"], timeout = 25)
        response.raise_for_status()
        data = response.json()

        if data.get("bizCode") != 10000:
            return (False, data.get("message", "Unknown error"))

        booking_code = data['data']['shareCode']
    
    except Exception as e:
        return (False, e)
    
    return (True, booking_code)

