from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError

import DatabaseLogic
import ORFSearch
import SearchGenefunction


# Auteur: Evander van Wolfswinkel
# Created: 2-3-2019
# Functionality: Used to render views that are linked to URL's
# Known Bugs: No known Bugs
# Renders index frontpage
def index(request):
    """Renders index"""
    return render(request, "index.html")


# Renders gene function page
def gene_function(request):
    """Renders gene_function page"""
    return render(request, "gene_function.html")


# Renders saved sequences page
def saved_sequences(request):
    """Renders page for loading up saved sequences"""
    return render(request, "saved_sequences.html")


def saved_sequences_result(request):
    """Renders saved_sequences as a result page"""
    try:
        orf_list = DatabaseLogic.loadORFS()
        ORFSearch.serializeORF(orf_list)
        return render(request, "ORFresult.html", {'orf_list': orf_list})
    except:
        return render(request, "error.html")



# Renders about page
def about(request):
    """Renders an about page"""
    return render(request, "about.html")


# Renders either a succes page, notifing that all orfs have been saved, or if operations was not succesfull an error page.
def ORFsaved(request):
    """Renders a succes page when storing the orf's has been an success."""
    orf_list = ORFSearch.deserializeORF()
    try:
        DatabaseLogic.storeORFS(orf_list)
        return render(request, "ORFsaved.html")
    except:
        return render(request, "error.html")

# Renders result page, handles 2 forms, one for file input and one for raw sequence input, when no value is given;
# - >render empty result page
def ORFresult(request):
    try:  # Try to get data from HTML forms using both raw input and file input
        if request.method == "POST":
            """If request method is POST; Check for file input and read raw sequence."""
            rawsequence = request.FILES['fasta'].read()
            inputtype = "file"  # Defines file input type
        if request.method == "GET":
            """If request method is GET; Check for raw input and use that."""
            rawsequence = request.GET.get("rawsequence")
            inputtype = "raw"  # Defines raw input type
    except MultiValueDictKeyError:  # Raise MultiValueDictKeyError when input is not given, render empty result page
        return render(request, "ORFresult.html")
    orf_list = ORFSearch.calculateORF(rawsequence, inputtype)
    """Calculates ORF based on the sequence and it's input type, input type is necessary for pre-processing."""
    ORFSearch.serializeORF(orf_list)
    """Serializes ORF list for later use."""
    return render(request, "ORFresult.html", {'orf_list': orf_list})


# Renders result from blasting found ORF's
def Blastresult(request):
    try:
        orf_list = ORFSearch.deserializeORF()
        """Deserializes ORF list into memory for use."""
        blast_results = SearchGenefunction.BLASTorf(orf_list)
        """Creates blast result list using ORF list input."""
        return render(request, "BLASTresult.html", {'blast_results': blast_results})
    except ValueError:  # render empty blast result page when no value is found
        return render(request, "BLASTresult.html")



# Renders result from blasting raw fasta sequence
def GeneFunctionresult(request):
    try:  # Try to get data from HTML form
        rawsequence = request.GET.get('rawsequence')
        """Uses GET method to get raw Fasta data from HTML form."""
        blast_results = SearchGenefunction.BLASTraw(str(rawsequence))
        """Creates blast result list using str input."""
        return render(request, "BLASTresult.html", {'blast_results': blast_results})
    except ValueError:  # Raise ValueError when no data is found from HTML form, render empty result page instead
        return render(request, "BLASTresult.html")
