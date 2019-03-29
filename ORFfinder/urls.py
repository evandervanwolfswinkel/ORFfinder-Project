from django.urls import path

from . import views

# Auteur: Evander van Wolfswinkel
# Created: 2-3-2019
# Functionality: URL patterns created for different views,
# these patterns are linked to corresponding HTML templates
# Known Bugs: No known Bugs

urlpatterns = [
    path('', views.index, name='index'),
    path('ORFresult/', views.ORFresult, name='ORFresult'),
    path('Blastresult/', views.Blastresult, name='Blastresult'),
    path('Genefunction/', views.gene_function, name='gene_function'),
    path('Genefunction/Result/', views.GeneFunctionresult, name='gene_functionresult'),
    path('Savedsequences/', views.saved_sequences, name='saved_sequences'),
    path('About/', views.about, name='about')


]