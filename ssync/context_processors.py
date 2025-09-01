SUPPORTED_SITES = ['Bet9ja', 'SportyBet']
sites_in_lower = [site.lower() for site in SUPPORTED_SITES]

logos = {
    'sportybet': 'img/sporty_logo.png',
    'bet9ja': 'img/b9_logo.png',
}

code_links = {
    'sportybet': 'https://www.sportybet.com/?shareCode={}=ng',
    'bet9ja': 'https://sports.bet9ja.com/?bookABetCode={}',
}

game_status = {
    'not start': 'pending',
    'ended': 'finished',
    'abandoned': 'finished',
    'none': 'pending',
    'h1': 'live',
    'h2': 'live',
    'ht': 'live',
    'live': 'live',
    'aet': 'finished',
    'ap': 'finished',
    'suspended': 'finished',
}



def site_list(request):
    sites = SUPPORTED_SITES
    return {'sites': sites, 'sites_lower': sites_in_lower}
