from datetime import datetime, timezone

sites_urls = {
    'Bet9ja': "https://coupon.bet9ja.com/desktop/feapi/CouponAjax/GetBookABetCoupon?couponCode={}&v_cache_version=1.279.0.198",
    'SportyBet': "https://www.sportybet.com/api/ng/orders/share/{}?_t={}"
}

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

list = ['over', 'under']
pick_interpretations = {
    '1X2': {
        '1': 'Home',
        '2': 'Away',
        'X': 'Draw',
    },
    'Over \/ Under': {
        
    }
}

def parse_overs_and_unders(pick, rest):
    try:
        for item in list:
            if item in pick.lower():
                _, num_str = rest.split('@')
                num = num_str.split('_')[0]
                pick = pick + f' {num}'

    except Exception as e:
        raise e
    
    return pick

# def translate_(home, away, pick):
#     if 'double chance' in pick.lower():
