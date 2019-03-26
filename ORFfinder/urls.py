from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ORFresult/', views.ORFresult, name='ORFresult'),
    path('Genefunction/', views.gene_function, name='gene_function'),
    path('Savedsequences/', views.saved_sequences, name='saved_sequences'),
    path('About/', views.about, name='about')


]