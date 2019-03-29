from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

import ORFSearch
import SearchGenefunction


# Auteur: Evander van Wolfswinkel
# Created: 2-3-2019
# Functionality: Used to render views that are linked to URL's
# Known Bugs: No known Bugs


def index(request):
    return render(request, "index.html")


def gene_function(request):
    return render(request, "gene_function.html")


def saved_sequences(request):
    return render(request, "saved_sequences.html")


def about(request):
    return render(request, "about.html")


# Renders result page, handles 2 forms, one for file input and one for raw sequence input, when no value is given;
# - >render empty result page
def ORFresult(request):
    try:
        if request.method == "POST":
            rawsequence = request.FILES['fasta'].read()
            inputtype = "file"
        if request.method == "GET":
            rawsequence = request.GET.get("rawsequence")
            inputtype = "raw"
    except MultiValueDictKeyError:
        return render(request, "ORFresult.html")
    orf_list = ORFSearch.calculateORF(rawsequence, inputtype)
    ORFSearch.serializeORF(orf_list)
    return render(request, "ORFresult.html", {'orf_list': orf_list})


# Renders result from blasting found ORF's
def Blastresult(request):
    orf_list = ORFSearch.deserializeORF()
    blast_results = SearchGenefunction.BLASTorf(orf_list)
    return render(request, "BLASTresult.html", {'blast_results': blast_results})


# Renders result from blasting raw fasta sequence
def GeneFunctionresult(request):
    rawsequence = request.GET.get('rawsequence')
    blast_results = SearchGenefunction.BLASTraw(str(rawsequence))
    return render(request, "BLASTresult.html", {'blast_results': blast_results})
