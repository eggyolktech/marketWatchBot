import urllib.request, json
from django.shortcuts import get_object_or_404, render

from .models import PriceAlert

def index(request):
    alert_list = PriceAlert.objects.order_by('effective_date')
    context = {'alert_list': alert_list}    
    return render(request, 'pricealert/index.html', context)
    
def filter(request, symbol_filter=None):
    if symbol_filter == "None":
        symbol_filter = None
    alert_list = PriceAlert.objects.filter(symbol=symbol_filter)
    alert_list = alert_list.order_by('effective_date')
    context = {'alert_list': alert_list}    
    return render(request, 'pricealert/index.html', context)