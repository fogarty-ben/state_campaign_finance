from django.shortcuts import render, get_object_or_404
from django.template import loader
from app.models import Campaignfinance


# Create your views here.
def index(request):
    return render(request, 'index.html')

def search_results(request):
    context = {key: val for key, val in request.POST.items() if val != ''}
    non_name = {key: val for key, val in request.POST.items() if key not in ['committee_name', 'committee_name', 'csrfmiddlewaretoken']}
    q1 = Campaignfinance.objects.filter(**non_name)
    print(q1)
    return render(request, 'search.html', context)


def contribution(request, contribution_id):
    contribution = get_object_or_404(Campaignfinance, pk=contribution_id)
    return render(request, 'contribution.html', {'contribution': contribution})
