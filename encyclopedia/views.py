from django import forms
from django.shortcuts import render, redirect
from django.urls import reverse
import random, markdown2

from . import util

#Index Page
#Displays links to all entries
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Entry Page
#Renders the contents of a wiki entry
def wiki(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title)),
        })
    else:
        return 

#Search
#Allows users to search for an entry. If none is found, display viable matches
def search(request):
    if request.method == "POST":
        query = request.POST['q']
        
        if query.lower() in [entry.lower() for entry in util.list_entries()]:
            return redirect("encyclopedia:wiki", title=query)

        else:
            matches = []
            for entry in util.list_entries():
                if query.lower() in entry.lower():
                    matches.append(entry)
                    
            return render(request, "encyclopedia/searchresults.html", {
                "query": query,
                "matches": matches
            })


#New Page
#Allows users to create their own wiki entries
#def new(request):
#    return render(request, "encyclopedia:new")

        
#Random Page
#Takes user to a random page
def random_page(request):
    rand = random.choice(util.list_entries())
    return redirect("encyclopedia:wiki", title=rand)