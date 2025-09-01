from .helpers import *
from .context_processors import *


def parse_and_scrape_sporty(id_, objs, dict_items, platforms):
    markets_all, tourneys_all = objs
    outcome = dict_items
    _, to_ = platforms
    field_name = tournament_attrs.get(to_)

    try:
        game_fields = parse_game_sporty_fields(outcome)
        if game_fields is None:
            return

        market_obj = get_market_object('sporty_id', markets_all, game_fields['market_id'])
        if market_obj:
            pick_txt = game_fields['pick'].lower()
            booking_data = create_booking_format(market_obj, pick_txt, game_fields['teams'], platforms)
            if booking_data:
                market_supported = True
            else:
                market_supported = False
            supported = True
        else:
            booking_data = None
            market_supported = False
            print('Market not supported', game_fields['market_type'])
            supported = False

        tourney_objs = get_tourney_objects('sporty_id', tourneys_all, game_fields['tourney_id'])
        tourney_ids = set([ getattr(tourney_obj, field_name) for tourney_obj in tourney_objs if getattr(tourney_obj, field_name) ])

        game_data = SimpleNamespace(
            id_ = str(id_),
            converted_to = to_,
            home_team = game_fields['home_team'],
            away_team = game_fields['away_team'],
            teams = game_fields['teams'],
            league = game_fields['league'], 
            start_time = game_fields['start_time'],
            expired = check_game_expiry(game_fields['start_time']),
            status = game_fields['status'], 
            market_type = game_fields['market_type'], 
            pick = game_fields['pick'], 
            odds = game_fields['odds'], 
            status_class = game_fields['status_class'], 
            supported = supported,
            tourney_ids = tourney_ids,
            booking_data = booking_data,
            market_supported = market_supported,
            market_id = game_fields['market_id'],
        )


    except Exception as e:
        raise e
    
    
    return game_data
    


def parse_and_scrape_b9(id_, objs, dict_items, platforms):
    markets_all, tourneys_all = objs
    key, val = dict_items
    _, to_ = platforms
    status = "Unknown"
    field_name = tournament_attrs.get(to_)

    try:
        game_fields = parse_game_b9_fields(key, val, status)
        if game_fields is None:
            return
        
        market_obj = get_market_object('b9_id', markets_all, game_fields['market_id'])
        if market_obj:
            pick_txt = clean_b9_pick(game_fields['rest'], market_obj.b9_prefix)
            booking_data = create_booking_format(market_obj, pick_txt, game_fields['teams'], platforms)
            if booking_data:
                market_supported = True
            else:
                market_supported = False
            supported = True
        else:
            print('Market not supported: ', game_fields['market_desc'])
            market_supported = False
            booking_data = None
            supported = False

        tourney_objs = get_tourney_objects('b9_id', tourneys_all, game_fields['tourney_id'])
        tourney_ids = set([ getattr(tourney_obj, field_name) for tourney_obj in tourney_objs if getattr(tourney_obj, field_name) ])

        game_data = SimpleNamespace(
            id_ = str(id_),
            converted_to = to_,
            home_team = game_fields['home'],
            away_team = game_fields['away'],
            teams = game_fields['teams'],
            league = game_fields['tournament'], 
            start_time = game_fields['start_time'], 
            expired = check_game_expiry(game_fields['start_time']),
            status = status, 
            market_type = game_fields['market_desc'],
            pick = game_fields['pick'], 
            odds = game_fields['odds'], 
            status_class = game_fields['status_class'],
            supported = supported,
            tourney_ids = tourney_ids,
            booking_data = booking_data,
            market_supported = market_supported,
            market_id = game_fields['market_id'],
        )


    except Exception as e:
        raise e

    return game_data