from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from django.db.models import Q

from .models import ForSaleBike, BikePhoto, Like, RideEvent, RidePhoto, EventComment, BIKE_TYPES

# ------------------------------
# Получение IP для лайков
# ------------------------------
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# ------------------------------
# Веломаркет
# ------------------------------
def bike_market(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('type')
    bikes = ForSaleBike.objects.all().order_by('-created_at')

    if query:
        bikes = bikes.filter(Q(title__icontains=query) | Q(brand__icontains=query))

    if filter_type:
        bikes = bikes.filter(type=filter_type)

    paginator = Paginator(bikes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/market.html', {
        'bikes': page_obj,
        'query': query,
        'filter_type': filter_type,
        'bike_types': BIKE_TYPES,
        'page_obj': page_obj,
    })

# ------------------------------
# Лайк для велосипеда
# ------------------------------
def like_bike(request, pk):
    bike = get_object_or_404(ForSaleBike, pk=pk)
    ip = get_client_ip(request)

    if not bike.likes.filter(ip_address=ip).exists():
        Like.objects.create(bike=bike, ip_address=ip)

    if request.headers.get('Hx-Request') == 'true':
        html = render_to_string('core/bike_like_block.html', {'bike': bike})
        return HttpResponse(html)

    return redirect('bike_market')

# ------------------------------
# Страница о команде
# ------------------------------
def about(request):
    return render(request, 'core/about.html')

# ------------------------------
# Список выездов команды
# ------------------------------
def ride_events(request):
    events = RideEvent.objects.all().order_by('-event_date', '-event_time')
    paginator = Paginator(events, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/ride_events.html', {
        'events': page_obj,
        'page_obj': page_obj,
    })

# ------------------------------
# Детальная страница выезда
# ------------------------------
def ride_event_detail(request, pk):
    event = get_object_or_404(RideEvent, pk=pk)
    comments = event.comments.all().order_by('-created_at')  # related_name='comments'
    return render(request, 'core/ride_event_detail.html', {
        'event': event,
        'comments': comments,
    })


def bike_detail(request, pk):
    bike = get_object_or_404(ForSaleBike, pk=pk)
    images = bike.images.all()
    return render(request, 'market/bike_detail.html', {
        'bike': bike,
        'images': images
    })
