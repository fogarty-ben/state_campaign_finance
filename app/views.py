from django.shortcuts import render, get_object_or_404
from django.template import loader


# Create your views here.
def index(request):
    return render(request, 'index.html')

def search_results(request):
    context = {key: val for key, val in request.POST.items() if val != ''}
    print(context)
    return render(request, 'search.html', context)


def contribution(request, contribution_id):
    #contribution = get_object_or_404(Contribution, pk=primary_key)
    return render(request, 'contribution.html', {'contribution_id': contribution_id})
