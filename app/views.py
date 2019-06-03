from django.shortcuts import render
from django.template import Context
from django.views.generic import ListView

# Create your views here.
def index(request):
    return render(request, 'index.html')

def search_results(request):
    context = {'query_terms': [request.GET['query']] * 5}
    print(request.GET)
    return render(request, 'search.html', context)

