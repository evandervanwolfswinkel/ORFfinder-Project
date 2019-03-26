from django.shortcuts import render

import ORFSearch


def index(request):
    return render(request, "index.html")


def gene_function(request):
    return render(request, "gene_function.html")


def saved_sequences(request):
    return render(request, "saved_sequences.html")


def about(request):
    return render(request, "about.html")

def ORFresult(request):
    rawsequence = request.GET.get('rawsequence')
    orf_list = ORFSearch.calculateORF(str(rawsequence))
    return render(request, "ORFresult.html", {'orf_list': orf_list})


def Blastresult(request):
    return render(request, "BLASTresult.html")
