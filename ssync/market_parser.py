import re


def handle_parsing_errors(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        
        except Exception as e:
            raise Exception(f'[{func.__name__}] Unexpected error: {e}')
        
    return wrapper

# B9

b9_dict_1x2 = {
    'home': '1',
    'draw': 'X',
    'away': '2',
    'home or draw': '1X', 
    'home or away': '12',         
    'draw or away': 'X2', 
}
b9_dict_1x2_1up = {
    'home': '11',
    'draw': 'X1',
    'away': '21',
}
b9_dict_1x2_2up = {
    'home': '12',
    'draw': 'X2',
    'away': '22',
}

b9_dict_home_none_away = {
    'home': '2',
    'none': 'X',
    'away': '2',
}
b9_dict_home_none_away_lastscore = {
    'home': '1',
    'none': 'N',
    'away': '2',
}

b9_dict_handicap = {
    'home': '1H',
    'draw': 'XH',
    'away': '2H',
}

b9_dict_ou = {
    'over': 'O',
    'under': 'U',
}
b9_dict_home_ou = {
    'over': 'OH',
    'under': 'UH',
}
b9_dict_away_ou = {
    'over': 'OA',
    'under': 'UA',
}
b9_dict_half_home_ou = {
    'over': 'HO',
    'under': 'HU',
}
b9_dict_half_away_ou = {
    'over': 'AO',
    'under': 'AU',
}
b9_dict_corner_home_ou = {
    'over': 'HCO',
    'under': 'HCU',
}
b9_dict_corner_away_ou = {
    'over': 'ACO',
    'under': 'ACU',
}

b9_dict_yes_no = {
    'yes': 'Y',
    'no': 'N',
}
b9_dict_yes_no_ggng = {
    'yes': 'GG',
    'no': 'NG',
}

b9_dict_odd_even = {
    'odd': 'OD',
    'even': 'EV',
}
b9_dict_odd_even_short = {
    'odd': 'O',
    'even': 'E',
}

b9_dict_cs = {
    'other': 'OTH',
}

b9_dict_multi = {
    '1-2': '1-2',
    '1-3': '1-3',
    '1-4': '1-4',
    '1-5': '1-5',
    '1-6': '1-6',
    '2-3': '2-3',
    '2-4': '2-4',
    '2-5': '2-5',
    '2-6': '2-6',
    '3-4': '3-4',
    '3-5': '3-5',
    '3-6': '3-6',
    '4-5': '4-5',
    '4-6': '4-6',
    '5-6': '5-6',
}
b9_dict_home_multi = {
    '1-2': 'HO12',  
    '1-3': 'HO13',  
    '2-3': 'HO23', 
}
b9_dict_away_multi = {
    '1-2': 'AW12',  
    '1-3': 'AW13',  
    '2-3': 'AW23', 
}
b9_dict_half_multi = {
    '1-2': '12',
    '1-3': '13',
    '1-3': '23',
}
b9_dict_multi_corner = {
    '0-8': '08',
    '12+': '12',
    '9-11': '911',
    '0-4': '04HT',
    '5-6': '56HT',
    '7+': '7HT',
}

b9_dict_both_only_none = {
    'only home': '1',
    'only away': '2',
    'none': 'NG',
    'both teams': 'GG',
}
 
b9_dict_dc_gg = {
    'home/draw & no': '1XNG',
    'home/draw & yes': '1XGG',
    'home/away & no': '12NG',
    'home/away & yes': '12GG',
    'away/draw & no': 'X2NG',
    'away/draw & yes': 'X2GG',
}
b9_dict_dc_gg_h = {
    'home/draw & no': '1XNGHT',
    'home/draw & yes': '1XGGHT',
    'home/away & no': '12NGHT',
    'home/away & yes': '12GGHT',
    'away/draw & no': 'X2NGHT',
    'away/draw & yes': 'X2GGHT',
}
b9_dict_dc_gg_hh = {
    'home/draw & no': '1XNG2T',
    'home/draw & yes': '1XGG2T',
    'home/away & no': '12NG2T',
    'home/away & yes': '12GG2T',
    'away/draw & no': 'X2NG2T',
    'away/draw & yes': 'X2GG2T',
}
b9_dict_1x2_gg = {
    'home & yes': '1ANDGG',
    'draw & yes': 'XANDGG',
    'away & yes': '2ANDGG',
    'home & no': '1ANDNG',
    'draw & no': 'XANDNG',
    'away & no': '2ANDNG',
}
b9_dict_1x2_gg_h = {
    'home & yes': '1HTANDGG',
    'draw & yes': 'XHTANDGG',
    'away & yes': '2HTANDGG',
    'home & no': '1HTANDNG',
    'draw & no': 'XHTANDNG',
    'away & no': '2HTANDNG',
}
b9_dict_1x2_gg_hh = {
    'home & yes': '12HTANDGG',
    'draw & yes': 'X2HTANDGG',
    'away & yes': '22HTANDGG',
    'home & no': '12HTANDNG',
    'draw & no': 'X2HTANDNG',
    'away & no': '22HTANDNG',
}
b9_dict_gg_over = {
    'over ||| & yes': 'GGO',
    'over ||| & no': 'NGO',
    'under ||| & yes': 'GGU',
    'under ||| & no': 'NGU',
}
b9_dict_gg_over_long = {
    'over ||| & yes': 'GGOVER',
    'over ||| & no': 'NGOVER',
    'under ||| & yes': 'GGUNDER',
    'under ||| & no': 'NGUNDER',
}
b9_dict_1x2_over = {
    'home & over |||': '1O',
    'draw & over |||': 'XO',
    'away & over |||': '2O',
    'home & under |||': '1U',
    'draw & under |||': 'XU',
    'away & under |||': '2U',
}
b9_dict_1x2_over_h = {
    'home & over |||': '1O1T',
    'draw & over |||': 'XO1T',
    'away & over |||': '2O1T',
    'home & under |||': '1U1T',
    'draw & under |||': 'XU1T',
    'away & under |||': '2U1T',
}
b9_dict_1x2_over_hh = {
    'home & over |||': '1O2T',
    'draw & over |||': 'XO2T',
    'away & over |||': '2O2T',
    'home & under |||': '1U2T',
    'draw & under |||': 'XU2T',
    'away & under |||': '2U2T',
}
b9_dict_dc_over = {
    'home/draw & over |||': '1XO',
    'home/draw & under |||': '1XU',
    'home/away & over |||': '12O',
    'home/away & under |||': '12U',
    'away/draw & over |||': 'X2O',
    'away/draw & under |||': 'X2U',
}

b9_dict_winmargin = {
    'draw': 'X',
    'home by 1': 'HT1',
    'home by 2': 'HT2',
    'home by 3+': 'HT>2',
    'away by 1': 'AT1',
    'away by 2': 'AT2',
    'away by 3+': 'AT>2',
}

b9_dict_ht_ft_ou = {
    '{home}/{home} & over |||': '1/1O',
    '{home}/draw & over |||': '1/XO',
    '{home}/{away} & over |||': '1/2O',
    '{home}/{home} & under |||': '1/1U',
    '{home}/draw & under |||': '1/XU',
    '{home}/{away} & under |||': '1/2U',
    'draw/{home} & over |||': 'X/1O',
    'draw/draw & over |||': 'X/XO',
    'draw/{away} & over |||': 'X/2O',
    'draw/{home} & under |||': 'X/1U',
    'draw/draw & under |||': 'X/XU',
    'draw/{away} & under |||': 'X/2U',
    '{away}/{home} & over |||': '2/1O',
    '{away}/draw & over |||': '2/XO',
    '{away}/{away} & over |||': '2/2O',
    '{away}/{home} & under |||': '2/1U',
    '{away}/draw & under |||': '2/XU',
    '{away}/{away} & under |||': '2/2U',
}
b9_dict_ht_ft_ou_h = {
    '{home}/{home} & over |||': '11O',
    '{home}/draw & over |||': '1XO',
    '{home}/{away} & over |||': '12O',
    '{home}/{home} & under |||': '11U',
    '{home}/draw & under |||': '1XU',
    '{home}/{away} & under |||': '12U',
    'draw/{home} & over |||': 'X1O',
    'draw/draw & over |||': 'XXO',
    'draw/{away} & over |||': 'X2O',
    'draw/{home} & under |||': 'X1U',
    'draw/draw & under |||': 'XXU',
    'draw/{away} & under |||': 'X2U',
    '{away}/{home} & over |||': '21O',
    '{away}/draw & over |||': '2XO',
    '{away}/{away} & over |||': '22O',
    '{away}/{home} & under |||': '21U',
    '{away}/draw & under |||': '2XU',
    '{away}/{away} & under |||': '22U',
}

b9_dict_most_half = {
    '1st half': '1',
    '2nd half': '2',
    'equal': 'E',
}

b9_dict_first_goal_1x2 = {
    'home goal & home': '1-1STGOAL1',
    'home goal & draw': '1-1STGOALX',
    'home goal & away': '1-1STGOAL2',
    'away goal & home': '2-1STGOAL1',
    'away goal & draw': '2-1STGOALX',
    'away goal & away': '2-1STGOAL2',
    'no goal': 'NOGOAL',
}



def create_b9_key(sign, market_obj):
    if sign:
        return f'{market_obj.b9_prefix}{sign}'
    return

def extract_ou_from_sporty(text):
    regex_ = r'(?:over|under)\s(\d+(?:\.\d+)?)'
    match = re.search(regex_, text)
    return match.group(1) if match else None

def split_handicap(pick_txt):
    pick_txt = pick_txt.removesuffix(')')
    pick, hcp = pick_txt.strip().split(' (')
    home, away = hcp.split(':')
    hcp = int(home) - int(away)
    return pick, hcp

def split_asian_handicap(pick_txt):
    pick_txt = pick_txt.removesuffix(')')
    pick, hcp = pick_txt.strip().split(' (')
    hcp = float(hcp)
    return pick, hcp

def convert_score_to_b9_format(score):
    score = score.replace(':', '-')
    return score

def split_sporty_multi_score(text):
    scores = re.split(r'\s*(?:or|,)\s+', text)
    return scores




@handle_parsing_errors
def b9_parse_1x2(pick_txt, market_obj, dict_ = None):
    sign = dict_.get(pick_txt)
    if sign:
        b9_key = create_b9_key(sign, market_obj)
        return b9_key
    
    return


@handle_parsing_errors
def b9_parse_handicap(pick_txt, market_obj, dict_ = None):
    pick, hcp = split_handicap(pick_txt)
    pick = dict_.get(pick)
    if pick:
        sign = f'{hcp}_{pick}'
        b9_key = create_b9_key(sign, market_obj)
        return b9_key
    
    return


@handle_parsing_errors
def b9_parse_asian_handicap(pick_txt, market_obj, dict_ = None):
    pick, hcp = split_asian_handicap(pick_txt)
    pick = dict_.get(pick)
    if pick:
        sign = f'{hcp}_{pick}'
        b9_key = create_b9_key(sign, market_obj)
        return b9_key
    
    return


@handle_parsing_errors
def b9_parse_over_under(pick_txt, market_obj, dict_ = None):
    o_u, num = pick_txt.strip().split(' ')
    pick = dict_.get(o_u)
    if pick:
        sign = f'{num}_{pick}'
        b9_key = create_b9_key(sign, market_obj)
        return b9_key

    return


@handle_parsing_errors
def b9_parse_correct_score(pick_txt, market_obj, dict_ = None):
    sign = dict_.get(pick_txt, pick_txt)
    b9_key = create_b9_key(sign, market_obj)
    return b9_key


@handle_parsing_errors
def b9_parse_htft_cs(pick_txt, market_obj, dict_ = None):
    htft_tuple = pick_txt.split(' ')
    hts, fts = map(convert_score_to_b9_format, htft_tuple)
    sign = f'{hts}/{fts}'
    b9_key = create_b9_key(sign, market_obj)
    return b9_key


@handle_parsing_errors
def b9_parse_exact_gcb(pick_txt, market_obj, dict_ = None):
    b9_key = create_b9_key(pick_txt, market_obj)
    return b9_key


@handle_parsing_errors
def b9_parse_htft_1x2(pick_txt, market_obj, dict_ = None):
    htft_tuple = pick_txt.split('/')
    ht, ft = map(dict.get, htft_tuple)
    if ht and ft:
        sign = f'{ht}/{ft}'
        b9_key = create_b9_key(sign, market_obj)
        return b9_key
    
    return


@handle_parsing_errors
def b9_parse_over_combinations(pick_txt, market_obj, dict_ = None):
    o_u = extract_ou_from_sporty(pick_txt)
    pick = pick_txt.replace(o_u, '|||')
    pick = dict_.get(pick)
    if pick:
        sign = f'{o_u}_{pick}'
        b9_key = create_b9_key(sign, market_obj)
        return b9_key
    
    return


@handle_parsing_errors    
def b9_parse_multi_score(pick_txt, market_obj, dict_ = None):
    scores = split_sporty_multi_score(pick_txt)
    if len(scores) > 1:
        scores = [ score.replace(':', '') for score in scores ]
        sign = ''.join(scores)
        b9_key = create_b9_key(sign, market_obj)
        return b9_key
    
    return 



        





dict_1x2 = {
    '1': 'Home',
    'X': 'Draw',
    '2': 'Away',
    '1X': 'Home or Draw',
    '12': 'Home or Away',        
    'X2': 'Draw or Away',
}

dict_over_and_under = {
    'O': 'Over',
    'U': 'Under',
    'HCO': 'Over',
    'HCU': 'Under',
    'ACO': 'Over',
    'ACU': 'Under',
    'HO': 'Over',
    'HU': 'Under',
    'AO': 'Over',
    'AU': 'Under',
    'OH': 'Over',
    'OA': 'Over',
    'UH': 'Under',
    'UA': 'Under',
}

dict_yes_no = {
    'Y': 'Yes',
    'N': 'No',
    'GG': 'Yes',
    'NG': 'No',
}

dict_odd_even = {
    'O': 'Odd',
    'E': 'Even',
    'OD': 'Odd',
    'EV': 'Even',
}

dict_home_none_away = {
    '1': 'Home',
    'X': 'None',
    'N': 'None',
    '2': 'Away'
}

dict_cs = {
    'OTH': 'Other'
}

dict_multi = {
    '1-2': '1-2',
    '1-3': '1-3',
    '1-4': '1-4',
    '1-5': '1-5',
    '1-6': '1-6',
    '2-3': '2-3',
    '2-4': '2-4',
    '2-5': '2-5',
    '2-6': '2-6',
    '3-4': '3-4',
    '3-5': '3-5',
    '3-6': '3-6',
    '4-5': '4-5',
    '4-6': '4-6',
    '5-6': '5-6',
    'HO12': '1-2', 
    'HO13': '1-3', 
    'HO23': '2-3',
    'AW12': '1-2', 
    'AW13': '1-3', 
    'AW23': '2-3',
    '12': '1-2', 
    '13': '1-3', 
    '23': '2-3',
}

dict_multi_corner = {
    '08': '0-8',
    '12': '12+',
    '911': '9-11',
    '04HT': '0-4',
    '56HT': '5-6',
    '7HT': '7+',
}

dict_both_only_none = {
    '1': 'Only Home',
    '2': 'Only Away',
    'NG': 'None',
    'GG': 'Both teams',
}

dict_dc_gg = {
    '1XNG': 'Home/Draw & No',
    '1XGG': 'Home/Draw & Yes',
    '12NG': 'Home/Away & No',
    '12GG': 'Home/Away & Yes',
    'X2NG': 'Away/Draw & No',
    'X2GG': 'Away/Draw & Yes',
    '1XNGHT': 'Home/Draw & No',
    '1XGGHT': 'Home/Draw & Yes',
    '12NGHT': 'Home/Away & No',
    '12GGHT': 'Home/Away & Yes',
    'X2NGHT': 'Away/Draw & No',
    'X2GGHT': 'Away/Draw & Yes',
    '1XNG2T': 'Home/Draw & No',
    '1XGG2T': 'Home/Draw & Yes',
    '12NG2T': 'Home/Away & No',
    '12GG2T': 'Home/Away & Yes',
    'X2NG2T': 'Away/Draw & No',
    'X2GG2T': 'Away/Draw & Yes',
}

dict_1x2_gg = {
    '1ANDGG': 'Home & yes',
    'XANDGG': 'Draw & yes',
    '2ANDGG': 'Away & yes',
    '1ANDNG': 'Home & no',
    'XANDNG': 'Draw & no',
    '2ANDNG': 'Away & no',
    '1HTANDGG': 'Home & yes',
    'XHTANDGG': 'Draw & yes',
    '2HTANDGG': 'Away & yes',
    '1HTANDNG': 'Home & no',
    'XHTANDNG': 'Draw & no',
    '2HTANDNG': 'Away & no',
    '12HTANDGG': 'Home & yes',
    'X2HTANDGG': 'Draw & yes',
    '22HTANDGG': 'Away & yes',
    '12HTANDNG': 'Home & no',
    'X2HTANDNG': 'Draw & no',
    '22HTANDNG': 'Away & no',
}

dict_gg_over = {
    'GGO': 'Over ||| & Yes',
    'NGO': 'Over ||| & No',
    'GGU': 'Under ||| & Yes',
    'NGU': 'Under ||| & No',
    'GGOVER': 'Over ||| & Yes',
    'NGOVER': 'Over ||| & No',
    'GGUNDER': 'Under ||| & Yes',
    'NGUNDER': 'Under ||| & No',
}

dict_1x2_over = {
    '1O': 'Home & Over |||',
    'XO': 'Draw & Over |||',
    '2O': 'Away & Over |||',
    '1U': 'Home & Under |||',
    'XU': 'Draw & Under |||',
    '2U': 'Away & Under |||',
    '1O1T': 'Home & Over |||',
    'XO1T': 'Draw & Over |||',
    '2O1T': 'Away & Over |||',
    '1U1T': 'Home & Under |||',
    'XU1T': 'Draw & Under |||',
    '2U1T': 'Away & Under |||',
    '1O2T': 'Home & Over |||',
    'XO2T': 'Draw & Over |||',
    '2O2T': 'Away & Over |||',
    '1U2T': 'Home & Under |||',
    'XU2T': 'Draw & Under |||',
    '2U2T': 'Away & Under |||',
}

dict_dc_over = {
    '1XO': 'Home/Draw & Over |||',
    '1XU': 'Home/Draw & Under |||',
    '12O': 'Home/Away & Over |||',
    '12U': 'Home/Away & Under |||',
    'X2O': 'Away/Draw & Over |||',
    'X2U': 'Away/Draw & Under |||',
}

dict_ht_ft_ou = {
    '11O': '{Home}/{Home} & over |||',
    '1XO': '{Home}/draw & over |||',
    '12O': '{Home}/{Away} & over |||',
    '11U': '{Home}/{Home} & under |||',
    '1XU': '{Home}/draw & under |||',
    '12U': '{Home}/{Away} & under |||',
    'X1O': 'draw/{Home} & over |||',
    'XXO': 'draw/draw & over |||',
    'X2O': 'draw/{Away} & over |||',
    'X1U': 'draw/{Home} & under |||',
    'XXU': 'draw/draw & under |||',
    'X2U': 'draw/{Away} & under |||',
    '21O': '{Away}/{Home} & over |||',
    '2XO': '{Away}/draw & over |||',
    '22O': '{Away}/{Away} & over |||',
    '21U': '{Away}/{Home} & under |||',
    '2XU': '{Away}/draw & under |||',
    '22U': '{Away}/{Away} & under |||',

}

dict_most_half = {
    '1': '1st half',
    '2': '2nd half',
    'E': 'Equal',
    'NG': 'No goal'
}

dict_winmargin = {
    'X': 'Draw',
    'HT1': 'Home by 1',
    'HT2': 'Home by 2',
    'HT>2': 'Home by 3+',
    'AT1': 'Away by 1',
    'AT2': 'Away by 2',
    'AT>2': 'Away by 3+',
}

dict_first_goal_1x2 = {
    '1-1STGOAL1': 'Home goal & Home',
    '1-1STGOALX': 'Home goal & Draw',
    '1-1STGOAL2': 'Home goal & Away',
    '2-1STGOAL1': 'Away goal & Home',
    '2-1STGOALX': 'Away goal & Draw',
    '2-1STGOAL2': 'Away goal & Away',
    'NOGOAL': 'No goal',
}








def is_even(num):
    try:
        num = int(num)
        if num % 2 == 0:    
            return True
        else:
            return False

    except Exception as e:
        print(f'Error: {e}')
        return


def punctuate_score(list_):
    try:
        punctuated = []
        for i in list_:
            if i == list[-1]:
                punctuated.append(f'or {i}')
            else:
                punctuated.append(f'{i},')
        return ' '.join(punctuated)

    except Exception as e:
        print(f'Error: {e}')
        return
    

def format_multiple_scores(str_):
    try:
        list_ = list(str_)
        scores_no = len(list_) // 2
        scores = []
        for i in range(scores_no):
            indx = i * 2
            score = f'{list_[indx]}:{list_[indx +1]}'
            scores.append(score)

        if list_[-1] == 'O':
            scores.append('Other')

        punctuated_str = punctuate_score(scores)

    except Exception as e:
        print(f'Error: {e}')
        punctuated_str = None

    return punctuated_str


def remove_string(value):
    try:
        if '.' in value:
            return float(value)
        else:
            return int(value)
        
    except Exception as e:
        print(f'Error: {e}')
        return


def split_ht_ft(pick_txt):
    if '/' in pick_txt:
        ht, ft = pick_txt.split('/')
        return (ht, ft)
    
    return None


def format_score(score):
    score = score.replace('-',':')
    return score
    

def convert_handicap_to_score(hcp):
    home, away = 0, 0
    hcp = remove_string(hcp)
    if hcp < 0:
        away -= hcp
    elif hcp >= 0:
        home += hcp
    
    return f'({home}:{away})'


def break_hcp_into_smaller_elements(pick_txt):
    pick_txt = pick_txt.removesuffix('H')
    hcp, pick = pick_txt.split('_')
    pick = dict_1x2.get(pick)

    return hcp, pick


def convert_handicap_to_numbers(hcp):
    hcp = remove_string(hcp)
    hcp_str = hcp
    if hcp >= 0 :
        hcp_str = '+' + f'{hcp}'
    
    return f'({hcp_str})'


def break_o_u_into_smaller_elements(pick_txt):
    o_u, pick = pick_txt.split('_')
    pick = dict_over_and_under.get(pick)
    return o_u, pick


def get_pick_obj(pick, market_obj):
    outcomes = market_obj.outcomes.all()
    pick_obj = None
    for outcome in outcomes:
        if outcome.desc.lower() == pick.lower():
            pick_obj = outcome
            break

    if pick_obj:
        return market_obj.sporty_id, market_obj.specifier, pick_obj.outcome_id
    
    return None





# PARSING FUNCTIONS

@handle_parsing_errors
def parse_1x2(pick_txt, market_obj, dict_ = None):
    if dict_ is None:
        dict_ = dict_1x2

    pick = dict_.get(pick_txt)
    pick_obj = get_pick_obj(pick, market_obj)

    return pick_obj


@handle_parsing_errors
def parse_1x2_up(pick_txt, market_obj, dict_ = None):
    pick_txt = pick_txt[:-1]
    pick = dict_.get(pick_txt)
    pick_obj = get_pick_obj(pick, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_over_and_under(pick_txt, market_obj, dict_ = None):
    o_u, pick = break_o_u_into_smaller_elements(pick_txt)
    pick_txt = f'{pick} {o_u}'
    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_handicap(pick_txt, market_obj, dict_ = None):
    hcp, pick = break_hcp_into_smaller_elements(pick_txt)
    score = convert_handicap_to_score(hcp)
    
    pick_txt = f'{pick} {score}'
    pick_obj = get_pick_obj(pick_txt, market_obj)

    return pick_obj


@handle_parsing_errors
def parse_asian_handicap(pick_txt, market_obj, dict_ = None):
    hcp, pick = break_hcp_into_smaller_elements(pick_txt)
    hcp_num = convert_handicap_to_numbers(hcp)

    pick_txt = f'{pick} {hcp_num}'
    pick_obj = get_pick_obj(pick_txt, market_obj)

    return pick_obj


@handle_parsing_errors
def parse_correct_score(pick_txt, market_obj, dict_ = None):
    pick_txt = dict_.get(pick_txt, pick_txt)

    htft_tuple = split_ht_ft(pick_txt)
    if htft_tuple:
        hts, fts = map(format_score, htft_tuple)
        pick_txt = f'{hts} {fts}'

    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_exact_gcb(pick_txt, market_obj, dict_ = None):
    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_ht_ft_1x2(pick_txt, market_obj, dict_ = None):
    htft_tuple = split_ht_ft(pick_txt)
    if htft_tuple:
        ht, ft = map(dict_.get, htft_tuple)
        pick_txt = f'{ht}/{ft}'

    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_over_combinations(pick_txt, market_obj, dict_ = None):
    ou, pick = pick_txt.split('_')
    pick_txt = dict_.get(pick)
    pick_txt = pick_txt.replace('|||', ou)
    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_multi_score(pick_txt, market_obj, dict_ = None):
    pick_txt = format_multiple_scores(pick_txt)
    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj


@handle_parsing_errors
def parse_ht_ft_ou(pick_txt, market_obj, dict_ = None):
    ou, pick = pick_txt.split('_')
    pick_txt = pick.replace('/', '')
    pick_txt = dict_.get(pick_txt)
    pick_txt = pick_txt.replace('|||', ou)

    pick_obj = get_pick_obj(pick_txt, market_obj)
    return pick_obj







DICTIONARIES = {
    'dict_1x2': dict_1x2,
    'dict_over_and_under': dict_over_and_under,
    'dict_yes_no': dict_yes_no,
    'dict_odd_even': dict_odd_even,
    'dict_home_none_away': dict_home_none_away,
    'dict_cs': dict_cs,
    'dict_multi': dict_multi,
    'dict_multi_corner': dict_multi_corner,
    'dict_both_only_none': dict_both_only_none,
    'dict_dc_gg': dict_dc_gg,
    'dict_1x2_gg': dict_1x2_gg,
    'dict_gg_over': dict_gg_over,
    'dict_1x2_over': dict_1x2_over,
    'dict_dc_over': dict_dc_over,
    'dict_ht_ft_ou': dict_ht_ft_ou,
    'dict_most_half': dict_most_half,
    'dict_winmargin': dict_winmargin,
    'dict_first_goal_1x2': dict_first_goal_1x2,

    'b9_dict_1x2': b9_dict_1x2,
    'b9_dict_1x2_1up': b9_dict_1x2_1up,
    'b9_dict_1x2_2up': b9_dict_1x2_2up,
    'b9_dict_home_none_away': b9_dict_home_none_away,
    'b9_dict_home_none_away_lastscore': b9_dict_home_none_away_lastscore,
    'b9_dict_handicap': b9_dict_handicap,
    'b9_dict_ou': b9_dict_ou,
    'b9_dict_home_ou': b9_dict_home_ou,
    'b9_dict_away_ou': b9_dict_away_ou,
    'b9_dict_half_home_ou': b9_dict_half_home_ou,
    'b9_dict_half_away_ou': b9_dict_half_away_ou,
    'b9_dict_corner_home_ou': b9_dict_corner_home_ou,
    'b9_dict_corner_away_ou': b9_dict_corner_away_ou,
    'b9_dict_yes_no': b9_dict_yes_no,
    'b9_dict_yes_no_ggng': b9_dict_yes_no_ggng,
    'b9_dict_odd_even': b9_dict_odd_even,
    'b9_dict_odd_even_short': b9_dict_odd_even_short,
    'b9_dict_cs': b9_dict_cs,
    'b9_dict_multi': b9_dict_multi,
    'b9_dict_home_multi': b9_dict_home_multi,
    'b9_dict_away_multi': b9_dict_away_multi,
    'b9_dict_half_multi': b9_dict_half_multi,
    'b9_dict_multi_corner': b9_dict_multi_corner,
    'b9_dict_both_only_none': b9_dict_both_only_none,
    'b9_dict_dc_gg': b9_dict_dc_gg,
    'b9_dict_dc_gg_h': b9_dict_dc_gg_h,
    'b9_dict_dc_gg_hh': b9_dict_dc_gg_hh,
    'b9_dict_1x2_gg': b9_dict_1x2_gg,
    'b9_dict_1x2_gg_h': b9_dict_1x2_gg_h,
    'b9_dict_1x2_gg_hh': b9_dict_1x2_gg_hh,
    'b9_dict_gg_over': b9_dict_gg_over,
    'b9_dict_gg_over_long': b9_dict_gg_over_long,
    'b9_dict_1x2_over': b9_dict_1x2_over,
    'b9_dict_1x2_over_h': b9_dict_1x2_over_h,
    'b9_dict_1x2_over_hh': b9_dict_1x2_over_hh,
    'b9_dict_dc_over': b9_dict_dc_over,
    'b9_dict_winmargin': b9_dict_winmargin,
    'b9_dict_ht_ft_ou': b9_dict_ht_ft_ou,
    'b9_dict_ht_ft_ou_h': b9_dict_ht_ft_ou_h,
    'b9_dict_most_half': b9_dict_most_half,
    'b9_dict_first_goal_1x2': b9_dict_first_goal_1x2,

}

PARSER_FUNCTIONS = {
    'parse_1x2': parse_1x2,
    'parse_1x2_up': parse_1x2_up,
    'parse_over_and_under': parse_over_and_under,
    'parse_handicap': parse_handicap,
    'parse_asian_handicap': parse_asian_handicap,
    'parse_correct_score': parse_correct_score,
    'parse_exact_gcb': parse_exact_gcb,
    'parse_ht_ft_1x2': parse_ht_ft_1x2,
    'parse_over_combinations': parse_over_combinations,
    'parse_multi_score': parse_multi_score,
    'parse_ht_ft_ou': parse_ht_ft_ou,

    'b9_parse_1x2': b9_parse_1x2,
    'b9_parse_handicap': b9_parse_handicap,
    'b9_parse_asian_handicap': b9_parse_asian_handicap,
    'b9_parse_over_under': b9_parse_over_under,
    'b9_parse_correct_score': b9_parse_correct_score,
    'b9_parse_htft_cs': b9_parse_htft_cs,
    'b9_parse_exact_gcb': b9_parse_exact_gcb,
    'b9_parse_htft_1x2': b9_parse_htft_1x2,
    'b9_parse_over_combinations': b9_parse_over_combinations,
    'b9_parse_multi_score': b9_parse_multi_score,
}