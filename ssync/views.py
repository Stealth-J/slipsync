from django.shortcuts import render
from .models import *
from .slip_scraper import *
from .context_processors import *
from render_block import render_block_to_string
from django.http import HttpResponse, JsonResponse
from .helpers import *
import ast


# Create your views here.
def home(request):
    return render(request, 'dashboard.html',)

def settings(request):
    return render(request, 'settings.html',)

def convert(request, platform):
    try:
        if platform.lower() not in sites_in_lower:
            return render(request, 'page_not_found.html')
        
        platform = platform.lower()
        platform_upper = SUPPORTED_SITES[sites_in_lower.index(platform.lower())]
        logo = logos.get(platform)
        
        
        if request.method == 'POST':
            slip_code = request.POST.get('slip_code')
            from_site = request.POST.get('from_site').lower()
            site = request.POST.get('site').lower()
            from_logo = logos.get(from_site)
            to_logo = logos.get(site)

            url = get_url(slip_code, from_site)
            platforms = (from_site, site)
            objs = (list(Market.objects.prefetch_related('parser_data', 'outcomes')), list(Tournament.objects.all()))

            success, slip_data = async_to_sync(parse_slip)(url, platforms, objs)

            if not success:
                raise Exception(slip_data)

            # slip_data = [ 
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '1',
            #         status_class="live",
            #         pick="Home Win",
            #         home_team="FC Barcelona",
            #         away_team="Real Madrid",
            #         market_type="Full Time Result",
            #         odds="2.10",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="La Liga",
            #         status="1st Half",
            #         supported=False,
            #         expired=True,
            #         market_supported=False,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '2',
            #         status_class="upcoming",
            #         pick="Over 2.5 Goals",
            #         home_team="Manchester United",
            #         away_team="Liverpool",
            #         market_type="Goals Over/Under",
            #         odds="1.85",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Premier League",
            #         status="Not Started",
            #         supported=True,
            #         expired=False,
            #         market_supported=False,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '3',
            #         status_class="finished",
            #         pick="Away Win",
            #         home_team="Bayern Munich",
            #         away_team="Borussia Dortmund",
            #         market_type="Full Time Result",
            #         odds="1.75",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Bundesliga",
            #         status="Full Time",
            #         supported=True,
            #         expired=False,
            #         market_supported=True,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '4',
            #         status_class="cancelled",
            #         pick="Draw",
            #         home_team="Juventus",
            #         away_team="AC Milan",
            #         market_type="Full Time Result",
            #         odds="3.20",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Serie A",
            #         status="Cancelled",
            #         supported=False,
            #         expired=True,
            #         market_supported=False,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '5',
            #         status_class="live",
            #         pick="Both Teams to Score",
            #         home_team="Paris Saint-Germain",
            #         away_team="Lyon",
            #         market_type="BTTS",
            #         odds="1.60",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Ligue 1",
            #         status="2nd Half",
            #         supported=True,
            #         expired=False,
            #         market_supported=True,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '6',
            #         status_class="upcoming",
            #         pick="Under 3.5 Goals",
            #         home_team="Ajax",
            #         away_team="PSV Eindhoven",
            #         market_type="Goals Over/Under",
            #         odds="1.90",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Eredivisie",
            #         status="Not Started",
            #         supported=True,
            #         expired=False,
            #         market_supported=False,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '7',
            #         status_class="finished",
            #         pick="Home Win",
            #         home_team="Chelsea",
            #         away_team="Arsenal",
            #         market_type="Full Time Result",
            #         odds="2.50",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Premier League",
            #         status="Full Time",
            #         supported=False,
            #         expired=True,
            #         market_supported=True,
            #         booking_data = 'We dont give a care ',
            #     ),
            #     SimpleNamespace(
            #         closest_match = ('Home Team', 'Away Team', '638975979'),
            #         converted_to = site,
            #         id_ = '8',
            #         status_class="suspended",
            #         pick="Over 1.5 Goals",
            #         home_team="Inter Milan",
            #         away_team="Napoli",
            #         market_type="Goals Over/Under",
            #         odds="1.40",
            #         start_time=datetime.now().strftime("%Y-%m-%d %H:%M"),
            #         league="Serie A",
            #         status="Suspended",
            #         supported=False,
            #         expired=True,
            #         market_supported=False,
            #         booking_data = 'We dont give a care ',
            #     ),
            # ]
            
            time_ = format_time(datetime.now(), ms = False)
            slip_link = code_links.get(from_site).format(slip_code)
            slip_data_raw = [ vars(data_) for data_ in slip_data ]
            ids_list = [ game.id_ for game in slip_data ]
            valid_selections = sum( 1 for game in slip_data if game.supported )

            context = {
                'slip_data': slip_data,
                'current_time': time_,
                'games_no': len(slip_data),
                'from_logo': from_logo,
                'to_logo': to_logo,
                'slip_link': slip_link,
                'slip_data_raw': slip_data_raw,
                'ids_list': ids_list,
                'valid_selections': valid_selections,
            }
            html = render_block_to_string('convert.html', 'slip_data_container', context, request)
            return HttpResponse(html)

        return render(request, 'convert.html', {'platform': platform_upper })
    
    except Exception as e:
        return render(request, 'error.html', {'message': e})



def edit_slip(request):
    removed_ = request.POST.get('removed_')
    ids_list = request.POST.get('ids_list')
    ids_list = ast.literal_eval(ids_list)
    edited_list = [ id_ for id_ in ids_list if id_ != removed_ ]
    response = HttpResponse('')
    response['HX-Trigger'] = json.dumps({"edited_list": edited_list})  # must be "" not ''
    return response


def sync(request):
    try:
        ids_list = request.POST.get('ids_list')
        slip_data = request.POST.get('slip_data')
        ids_list, slip_data = ast.literal_eval(ids_list), ast.literal_eval(slip_data)
        valid_games, to_ = filter_game_slip_final(slip_data, ids_list)

        booking_func = dict_booking.get(to_)
        success, booking_code = booking_func(valid_games)
        if not success:
            raise Exception(booking_code)

        return render(request, 'booking_code.html', {'booking_code': booking_code})

    except Exception as e:
        return render(request, 'booking_code.html', {'error': e})


def contact(request):
    return render(request, 'contact.html')

def help(request):
    return render(request, 'help.html')