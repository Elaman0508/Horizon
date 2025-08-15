from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template.loader import render_to_string
from .models import Rider, Like
from django.core.paginator import Paginator
from .models import ForSaleBike
from django.db.models import Q


def get_client_ip(request):
    """Получаем IP пользователя"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    riders = Rider.objects.all()
    sorted_riders = sorted(riders, key=lambda r: r.likes.count(), reverse=True)

    for rider in sorted_riders:
        rider.likes_count = rider.likes.count()

    paginator = Paginator(sorted_riders, 6)  # по 6 карточек на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/home.html', {'page_obj': page_obj})

def rider_detail(request, pk):
    """Страница участника"""
    rider = get_object_or_404(Rider, pk=pk)
    rider.likes_count = rider.likes.count()
    return render(request, 'core/rider_detail.html', {'rider': rider})


def like_rider(request, pk):
    """Добавить лайк и обновить блок без перезагрузки"""
    rider = get_object_or_404(Rider, pk=pk)
    ip = get_client_ip(request)

    if not rider.likes.filter(ip_address=ip).exists():
        Like.objects.create(rider=rider, ip_address=ip)

    # HTMX: возвращаем только HTML блок с лайками
    if request.headers.get('Hx-Request') == 'true':
        html = render_to_string('core/like_block.html', {'rider': rider})
        return HttpResponse(html)

    return redirect('rider_detail', pk=pk)


def bike_rating(request):
    """Рейтинг велосипедов"""
    riders = Rider.objects.filter(bike__isnull=False)
    sorted_riders = sorted(riders, key=lambda r: r.likes.count(), reverse=True)

    for rider in sorted_riders:
        rider.likes_count = rider.likes.count()

    return render(request, 'core/bike_rating.html', {'riders': sorted_riders})


def about(request):
    return render(request, 'core/about.html')

def market(request):
    query = request.GET.get('q')
    filter_type = request.GET.get('type')
    bikes = ForSaleBike.objects.all().order_by('-created_at')

    if query:
        bikes = bikes.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(type__icontains=query)
        )

    if filter_type:
        bikes = bikes.filter(type=filter_type)

    return render(request, 'core/market.html', {'bikes': bikes, 'query': query, 'filter_type': filter_type})
