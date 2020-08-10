from django.shortcuts import render, redirect
from django.urls import reverse
import random, markdown2

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def wiki(request, title):
    if util.get_entry(title):
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": markdown2.markdown(util.get_entry(title)),
        })
    else:
        return render(request, "encyclopedia/error.html")

def random_page(request):
    rand = random.choice(util.list_entries())
    return redirect("encyclopedia:wiki", title=rand)