from django.shortcuts import render

import ORFSearch


# Create your views here.
def index(request):
    return render(request, "index.html")


def ORFresult(request):
    rawsequence = request.GET.get('rawsequence')
    orf_list = ORFSearch.calculateORF(str(rawsequence))

    return render(request, "test.html", {'orf_list': orf_list})
