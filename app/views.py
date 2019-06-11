from django.shortcuts import render, get_object_or_404
from django.template import loader
from app.models import contributions, interested_user
from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def interested(request):
    user = interested_user()
    user.email = request.POST['email']
    user.interested_state = request.POST['state']
    user.save()
    return HttpResponseRedirect(reverse("index"))


def search_results(request):
    context = {key: val for key, val in request.GET.items() if val != ''}
    
    q = contributions.objects.all()
    if 'committee_name' in context:
        q = q.filter(committee_name__search=context['committee_name'])
    if 'committee_state' in context:
        q = q.filter(committee_state=context['committee_state'])
    if 'contrib_full_name' in context:
        q = q.filter(contrib_full_name__search=context['contrib_full_name'])
    if 'contrib_zip' in context:
        q = q.filter(contrib_zip=context['contrib_zip'])
    if 'contrib_state' in context:
        q = q.filter(contrib_state=context['contrib_state'])
    if 'contrib_occupation' in context:
        q = q.filter(contrib_occupation__search=context['committee_name'])
    if 'contrib_employer' in context:
        q = q.filter(contrib_employer__search=context['contrib_full_name'])
    if 'min_amount' in context:
        q = q.filter(amount__gte=context['min_amount'])
    if 'max_amount' in context:
        q = q.filter(amount__lte=context['max_amount'])
    if 'start_date' in context:
        q = q.filter(date__gte=datetime.strptime(context['start_date'], '%Y-%m-%d').date())
    if 'end_date' in context:
        q = q.filter(date__lte=datetime.strptime(context['end_date'], '%Y-%m-%d').date())

    p = Paginator(q, 25)
    context['results'] = p.get_page(int(context.get('page', 1)))
    return render(request, 'search.html', context)

def contribution(request, contribution_id):
    contribution = get_object_or_404(Campaignfinance, pk=contribution_id)
    return render(request, 'contribution.html', {'contribution': contribution})
