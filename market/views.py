from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.template.loader import render_to_string
from django.http import HttpResponse

from core.models import ForSaleBike, Like


def bike_market(request):
    """Главная страница маркет-раздела"""
    bikes = ForSaleBike.objects.all().order_by('-created_at')

    paginator = Paginator(bikes, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'market/market.html', {
        'page_obj': page_obj
    })


def bike_detail(request, pk):
    bike = get_object_or_404(ForSaleBike, pk=pk)

    similar_bikes = ForSaleBike.objects.filter(
        type=bike.type
    ).exclude(id=bike.id)[:4]

    return render(request, 'market/bike_detail.html', {
        'bike': bike,
        'similar_bikes': similar_bikes
    })


def like_bike(request, pk):
    """Лайк велосипеда (HTMX)"""
    bike = get_object_or_404(ForSaleBike, pk=pk)
    ip = request.META.get('REMOTE_ADDR')

    if not Like.objects.filter(bike=bike, ip_address=ip).exists():
        Like.objects.create(bike=bike, ip_address=ip)

    if request.headers.get('Hx-Request') == 'true':
        html = render_to_string(
            'market/bike_like_block.html',
            {'bike': bike}
        )
        return HttpResponse(html)

    return redirect('bike_market')
