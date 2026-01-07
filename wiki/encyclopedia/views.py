from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse
from markdown2 import Markdown
import random
import pdb
import ipdb

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    entry = util.get_entry(title)
    markdowner = Markdown()
    entry_html = markdowner.convert(str(entry))
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "entry_html": entry_html
    })
    
def random_page(request):
    print("random called")
    entries_list = util.list_entries()
    print(entries_list)
    random_entry = random.choice(entries_list)
    print(random_entry)
    return HttpResponseRedirect(reverse("page", args=[random_entry]))
    # return HttpResponse("random")

def create_entry(request):
    return render(request, "encyclopedia/new_entry.html")

def search(request):
    ...