from django import forms
from django.contrib import messages
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

    #Render error page if the requested entry does not exist
    else:
        return render(request, "encyclopedia/error.html")

#Search
#Allows users to search for an entry. If none is found, display viable matches
def search(request):
    if request.method == "POST":
        query = request.POST["q"]

        #Check if there's any entry that exactly matches the user's input
        if query.lower() in [entry.lower() for entry in util.list_entries()]:
            return redirect("encyclopedia:wiki", title=query)

        #Otherwise, display all entries that contain the user's input as a substring
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

        #Display error message if an entry already exists with the provided title
        if title.lower() in [entry.lower() for entry in util.list_entries()]:
            messages.error(request,"Error: A wiki entry with that name already exists.")
            return redirect("encyclopedia:create")

        #Save the user's input as a new entry, and append the title as a heading
        else: 
            titled_content = "#"+title+"\n\n"+content
            util.save_entry(title, titled_content)
            return redirect("encyclopedia:wiki", title=title)

    else:
        return render(request, "encyclopedia/create.html")

#Edit Page
#Allows users to edit existing entries
def edit(request, title):
    content = util.get_entry(title)
    if content:
        if request.method == "POST":
            #Delete the entry if no content was given
            if not request.POST["edited_content"]:
                util.delete(title)
                return redirect("encyclopedia:index")
            
            #Otherwise, save the updated entry
            else:
                util.save_entry(title, request.POST["edited_content"])
                return redirect("encyclopedia:wiki", title=title)

        #If request method isn't post, render a page where the user can edit the entry
        else:
            return render(request, "encyclopedia/edit.html", {
                "title": title,
                "content": content
            })

    #Render error page if the user tries to edit an entry that doesn't exist
    else:
        return render(request, "encyclopedia/error.html")

#Random Page
#Takes user to a random page
def random_page(request):
    rand = random.choice(util.list_entries())
    return redirect("encyclopedia:wiki", title=rand)