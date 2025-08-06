from datetime import datetime, timezone
from functools import wraps
import time

sites_urls = {
    'Bet9ja': "https://coupon.bet9ja.com/desktop/feapi/CouponAjax/GetBookABetCoupon?couponCode={}&v_cache_version=1.279.0.198",
    'SportyBet': "https://www.sportybet.com/api/ng/orders/share/{}?_t={}"
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


def handle_parsing_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except Exception as e:
            raise Exception(f'[{func.__name__}] Unexpected error: {e}')
        
    return wrapper



def format_time(time_data, ms = True):
    ms_time = time_data
    if ms:
        ms_time = datetime.fromtimestamp(time_data / 1000, tz=timezone.utc)
    
    time = ms_time.strftime("%I:%M %p · %B %d, %Y")
    return time[1:] if time.startswith('0') else time


def get_url(slip_code, platform):
    url_raw = sites_urls.get(platform, None)
    timestamp = get_timestamp(platform)

    url = url_raw.format(slip_code, timestamp)

    return url

def get_timestamp(platform, time_raw = None):
    if platform == 'SportyBet':
        dt = datetime.now()

    elif platform == 'Bet9ja':
        if time_raw == None:
            return None

        dt = datetime.strptime(time_raw, "%Y-%m-%d %H:%M:%S")
    
    timestamp = int(dt.timestamp() * 1000)

    return timestamp



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


