from django.shortcuts import render
from .models import *
from .slip_scraper import *
from .context_processors import *
from render_block import render_block_to_string
from django.http import HttpResponse
from .helpers import *
import ast
from django.contrib.admin.views.decorators import staff_member_required
from collections import defaultdict
from django.db.models import Q


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
            
            unrecognized_markets  = [ (each.market_id, each.market_type) for each in slip_data if not each.market_supported ]
            ns_markets_objs = []
            for unrec in unrecognized_markets:
                id_, name_ = unrec
                if not NotSupportedMarket.objects.filter(identifier = id_).exists():
                    ns_markets_objs.append(NotSupportedMarket(identifier = id_, market_platform = from_site, name = name_))

            NotSupportedMarket.objects.bulk_create(ns_markets_objs)
            
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
    response['HX-Trigger'] = json.dumps({"edited_list": edited_list}) 
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


@staff_member_required
def admin_tourneys(request):
    unsupported_tournaments = NotSupportedTournament.objects.all().order_by('country')
    tournaments = Tournament.objects.all().order_by('country')

    grouped = defaultdict(list)
    for obj in NotSupportedTournament.objects.all():
        grouped[obj.country].append(obj)

    if request.method == 'POST':
        print(request.POST, '|||---')
        query = request.POST.get('query').strip()
        active_tab = request.POST.get('active_tab')

        unsupported_tournaments = unsupported_tournaments.filter( 
            Q(identifier__icontains = query) | Q(market_platform__icontains = query) | Q(country__icontains = query) | Q(tourney_name__icontains = query)
         )
        tournaments = tournaments.filter( 
            Q(sporty_id__icontains = query) | Q(sporty_name__icontains = query) | Q(b9_id__icontains = query) | Q(b9_name__icontains = query) | Q(country__icontains = query)
        )
        
        context = {'unsupported_tournaments': unsupported_tournaments, 'tournaments': tournaments}
        html = render_block_to_string('admin_tourneys.html', active_tab, context)
    
        return HttpResponse(html)

    context = {
        'unsupported_tournaments': unsupported_tournaments,
        'tournaments': tournaments,
        'countries': list(NotSupportedTournament.objects.values_list('country', flat = True))
    }

    return render(request, "admin_tourneys.html", context)


@staff_member_required
def tourney_create(request):
    try:
        ids = request.POST.getlist('identifier')
        remove_rows = request.POST.getlist('ids_selected')
        if len(ids) != 2:
            message = 'Pick one of each platform only'
            remove_rows = []
        else:
            if both_platforms_represented(ids):
                ids = sorted(ids, key = lambda x: x)
                new_ids = []
                for id_ in ids:
                    _, identifier, tourney_name, country = id_.split("||")
                    new_ids.append((identifier, tourney_name, country))
                b9, sporty = new_ids
                b9_id, b9_name, b9_country = b9
                sporty_id, sporty_name, _ = sporty
                
                if Tournament.objects.filter(b9_id = b9_id, sporty_id = sporty_id, b9_name = b9_name, sporty_name = sporty_name, country = b9_country).exists():
                    message = 'The tournament object is already created'
                else:
                    Tournament.objects.create(b9_id = b9_id, sporty_id = sporty_id, b9_name = b9_name, sporty_name = sporty_name, country = b9_country)
                    NotSupportedTournament.objects.filter(identifier__in = (b9_id, sporty_id)).delete()
                    message = 'Tournament object created successfully'

            else:
                message = 'You cannot pick two objects from the same platform'
                remove_rows = []
    
    except:
        message = 'An error occured. Try again'
        remove_rows = []
        
    response = HttpResponse("")
    response['HX-Trigger'] = json.dumps({'message_': message, 'remove_rows': remove_rows })
    return response


@staff_member_required
def tourney_filter(request):
    filtered = Tournament.objects.filter(Q(sporty_id = None) | Q(b9_id = None))
    context = {'tournaments': filtered}
    html = render_block_to_string('admin_tourneys.html', 'supported_table', context)
    return HttpResponse(html)


@staff_member_required
def tourney_update(request):
    try:
        tournaments_all = list(Tournament.objects.all())
        ids_selected = request.POST.getlist('ids_selected')
        updated_tuples = []
        updated_tourney_objs = []

        for key, value in request.POST.lists():
            key_num = key.removeprefix('obj_id_')
            if key_num in ids_selected:
                value.append(key_num)
                updated_tuples.append(value )

        if updated_tuples:
            for obj_tuple in updated_tuples:
                try:
                    b9, sporty, tourney_id = obj_tuple
                    tourney_obj = None
                    updated = False

                    for t_obj in tournaments_all:
                        if t_obj.id == int(tourney_id):
                            tourney_obj = t_obj
                            break

                    if tourney_obj:
                        if update_field(b9):
                            b9_id, b9_name = b9.split('||')
                            tourney_obj.b9_id = b9_id
                            tourney_obj.b9_name = b9_name
                            updated = True
                            NotSupportedTournament.objects.filter(identifier = b9_id, tourney_name = b9_name).delete()
                        if update_field(sporty):
                            sporty_id, sporty_name = sporty.split('||')
                            tourney_obj.sporty_id = sporty_id
                            tourney_obj.sporty_name = sporty_name
                            updated = True
                            NotSupportedTournament.objects.filter(identifier = sporty_id, tourney_name = sporty_name).delete()
                        if updated:
                            updated_tourney_objs.append(tourney_obj)

                except Exception as e:
                    print(f'Error: {e}')
                    continue
            
            message = f'{len(updated_tourney_objs)} object(s) updated successfully'
            Tournament.objects.bulk_update(updated_tourney_objs, ['sporty_id', 'sporty_name', 'b9_id', 'b9_name'])

        else:
            message = 'Select a tournament'

    except Exception as e:
        message = 'An error occured'
        print(f'Error: {e}')

    response = HttpResponse('')
    response['HX-Trigger'] = json.dumps({'message_': message })
    return response


@staff_member_required
def tourney_delete(request, pk):
    try:
        remove_rows = request.POST.getlist('ids_selected')
        ids_selected = [ int(id_) for id_ in remove_rows ]

        if pk == 'unregistered':
            objs_to_delete = NotSupportedTournament.objects.filter(id__in = ids_selected)

        elif pk == 'registered':
            objs_to_delete = Tournament.objects.filter(id__in = ids_selected)
            remove_rows = [f'_{id_}' for id_ in remove_rows ]

        if objs_to_delete:
            message = f'{len(objs_to_delete)} object(s) deleted successfully'
            objs_to_delete.delete()
        else:
            message = 'Objects dont exist'
            if len(ids_selected) == 0:
                message = 'Select a tournament'
            remove_rows = []

    except Exception as e:
        message = 'An error occured'
        remove_rows = []
        print(f'Error: {e}')


    response = HttpResponse('')
    response['HX-Trigger'] = json.dumps({'message_': message, 'remove_rows': remove_rows})
    return response


def admin_markets(request):
    un_markets = NotSupportedMarket.objects.all()
    context = {'un_markets': un_markets}
    return render(request, 'admin_markets.html', context)