from django.shortcuts import render
from .models import *
from .slip_scraper import *
from .context_processors import *
from render_block import render_block_to_string
from django.http import HttpResponse
from .helpers import *
import math


# Create your views here.
def home(request):
    return render(request, 'dashboard.html', {'text': 'Enabhorena'})

def settings(request):
    return render(request, 'settings.html', {'text': 'Enabhorena'})

def convert(request, platform):
    if platform.lower() not in sites_in_lower:
        return render(request, 'page_not_found.html')
    
    platform = SUPPORTED_SITES[sites_in_lower.index(platform.lower())]
    logo = logos.get(platform.lower())
    
    
    if request.method == 'POST':
        slip_code = request.POST.get('slip_code')
        site = request.POST.get('site')

        url = get_url(slip_code, site)

        success, slip_data = parse_slip(url, site)

        if not success:
            return render(request, 'error.html', {'message': slip_data})
        
        time = format_time(datetime.now(), ms = False)
        odds_list = [ game.odds for game in slip_data]
        total = math.prod(odds_list)

        context = {
            'slip_data': slip_data,
            'current_time': time,
            'games_no': len(slip_data),
            'logo': logo,
            'total': round(total, 2)
        }
        html = render_block_to_string('convert.html', 'slip_data_container', context, request)
        return HttpResponse(html)

    return render(request, 'convert.html', {'platform': platform })

def contact(request):
    return render(request, 'contact.html')

def help(request):
    return render(request, 'help.html')