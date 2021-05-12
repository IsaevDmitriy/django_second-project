from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.conf import settings
import csv



def index(request):
    return redirect(reverse(bus_stations))


def bus_stations(request):
    path = settings.BUS_STATION_CSV
    with open(path, encoding="cp1251", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        CONTENT = [{'Name': item['Name'], 'Street': item['Street'], 'District': item['District']} for item in reader]
    paginator = Paginator(CONTENT, 10)
    number = int(request.GET.get('page', 1))
    if 0 < number <= paginator.num_pages:
        page_number = number
    else:
        page_number = 1
    page = paginator.get_page(page_number)
    content = page.object_list
    current_page = page_number
    if page_number < paginator.num_pages:
        next_page_url = f'bus_stations?page={page.next_page_number()}'
    else:
        next_page_url = None
    if page_number > 1:
        prev_page_url = f'bus_stations?page={page.previous_page_number()}'
    else:
        prev_page_url = None

    return render(request, 'index.html', context={
        'bus_stations': content,
        'current_page': current_page,
        'prev_page_url': prev_page_url,
        'next_page_url': next_page_url,
    })
