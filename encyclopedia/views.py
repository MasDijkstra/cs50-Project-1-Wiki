from django import forms
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
import random, markdown2

from . import util

class CreatePageForm(forms.Form):
    title = forms.CharField(max_length = 60)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":10, "cols":10}))

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
        query = request.POST["q"]
        
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

#Create Page
#Allows users to create their own wiki entries
def create(request):
    if request.method == "POST":
        title, content = request.POST["title"], request.POST["content"]

        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            messages.error(request,"Error: A wiki entry with that name already exists.")
            return redirect("encyclopedia:create")

        else: 
            util.save_entry(title, content)
            return redirect("encyclopedia:wiki", title=title)

    else:
        return render(request, "encyclopedia/create.html")

#Edit Page
#Allows users to edit existing entries
def edit(request):
    pass


#Random Page
#Takes user to a random page
def random_page(request):
    rand = random.choice(util.list_entries())
    return redirect("encyclopedia:wiki", title=rand)