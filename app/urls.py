from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search_results, name='search'),
    path('contribution/<str:contribution_id>', views.contribution, name='contribution'),
    path('interested', views.interested, name='interested'),
]
