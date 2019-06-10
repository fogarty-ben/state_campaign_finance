from django.shortcuts import render
from django.template import Context
from django.views.generic import ListView

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search_results(request):
    context = {key: val for key, val in request.POST.items() if val != ''}
    print(context)
    return render(request, 'search.html', context)

