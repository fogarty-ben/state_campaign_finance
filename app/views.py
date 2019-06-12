from django.shortcuts import render, get_object_or_404
from django.template import loader
from app.models import contributions, interested_user
from datetime import datetime
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector


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
    
    query = """
                SELECT *
                FROM financelarge
                WHERE {}
                """
    where_clause = []
    params = {}
    if 'committee_state' in context:
        append = """
                 (committee_state = %(committee_state)s)
                 """
        where_clause.append(append)
        params['committee_state'] = context['committee_state']
    if 'contrib_zip' in context:
        append = """
                 (contrib_zip = %(contrib_zip)s)
                 """
        where_clause.append(append)
        params['contrib_zip'] = context['contrib_zip']
    if 'contrib_state' in context:
        append = """
                 (contrib_state = %(contrib_state)s)
                 """
        where_clause.append(append)
        params['contrib_state'] = context['contrib_state']
    if 'min_amount' in context:
        append = """
                 (amount >= %(min_amount)s)
                 """
        where_clause.append(append)
        params['min_amount'] = int(context['min_amount'])
    if 'max_amount' in context:
        append = """
                 (amount <= %(max_amount)s)
                 """
        where_clause.append(append)
        params['max_amount'] = context['max_amount']
    if 'start_date' in context:
        append = """
                 (date >= DATE(%(start_date)s))
                 """
        where_clause.append(append)
        params['start_date'] = context['start_date']
    if 'end_date' in context:
        append = """
                 (date <= DATE(%(end_date)s))
                 """
        where_clause.append(append)
        params['end_date'] = context['end_date']
    if 'committee_name' in context:
        append = """
                 (to_tsvector('english', committee_name) @@ plainto_tsquery('english', %(committee_name)s))
                 """
        where_clause.append(append)
        params['committee_name'] = context['committee_name']
    if 'contrib_name' in context:
        append = """
                (to_tsvector('english', contrib_first) @@ plainto_tsquery('english', %(contrib_name)s) OR
                to_tsvector('english', contrib_middle) @@ plainto_tsquery('english', %(contrib_name)s) OR
                to_tsvector('english', contrib_last) @@ plainto_tsquery('english', %(contrib_name)s) OR
                to_tsvector('english', contrib_org) @@ plainto_tsquery('english', %(contrib_name)s))
                """
        where_clause.append(append)
        params['contrib_name'] = context['contrib_name']
    if 'contrib_occupation' in context:
        append = """
                 (to_tsvector('english', contrib_occupation) @@ plainto_tsquery('english', %(contrib_occupation)s))
                 """
        where_clause.append(append)
        params['contrib_occupation'] = context['contrib_occupation']
    if 'contrib_employer' in context:
        append = """
                 (to_tsvector('english', contrib_employer) @@ plainto_tsquery('english', %(contrib_employer)s))
                 """
        where_clause.append(append)
        params['contrib_employer'] = context['contrib_employer']
    where_clause = " AND ".join(where_clause)
    q = contributions.objects\
                     .raw(query.format(where_clause), params)

    p = Paginator(q, 25)
    context['results'] = p.get_page(int(context.get('page', 1)))
    return render(request, 'search.html', context)

def contribution(request, contribution_id):
    contribution = get_object_or_404(contributions, pk=contribution_id)
    return render(request, 'contribution.html', {'contribution': contribution})
