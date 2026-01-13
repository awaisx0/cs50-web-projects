from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponse, Http404
from markdown2 import Markdown
import random

from .forms import NewPageForm, EditPageForm
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def page(request, title):
    entry = util.get_entry(title)
    
    # render 404 page
    if not entry:
        raise Http404("Requested page not found")
    
    # markdown to html conversion
    markdowner = Markdown()
    entry_html = markdowner.convert(str(entry))
    
    return render(request, "encyclopedia/page.html", {
        "title": title,
        "entry_html": entry_html
    })
    
    
def search(request):
    # get q from query params
    query = request.GET.get("q")
    
    # if seach query matches an entry, redirect to entry page
    entry = util.get_entry(query)
    if entry:
        return HttpResponseRedirect(reverse("page", args=[query]))
    
    entries_list = util.list_entries()
    
    search_results = []
    for entry in entries_list:
        # check if query is substring of entry, then append to search results
        if query in entry:
            search_results.append(entry)
            
    return render(request, "encyclopedia/search_results.html", {
        "search_results": search_results
    })
    
    
    
def new_page(request):
    if request.method == "POST":
        # title = request.POST.get("title")
        # content = request.POST.get("content")
        
        page_form = NewPageForm, EditPageForm(request.POST)
        
        if page_form.is_valid():
            title = page_form.cleaned_data.get("title")
            content = page_form.cleaned_data.get("content")
            

            # if a an entry is already added with same title
            entries_list = util.list_entries()
            if title in entries_list:
                raise Http404("entry with this title already exists")
            
            # success and saving entry
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("page", args=[title]))
        
        else:
            return render(request, "encyclopedia/new_page.html", {
                "form": page_form
            })
            
    
    return render(request, "encyclopedia/new_page.html", {
        "form": NewPageForm(),
    })
    
def edit_page(request, title):
    if request.method == "POST":
        page_form = EditPageForm(request.POST)
        
        if page_form.is_valid():
            content = page_form.cleaned_data.get("content")
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("page", args=[title]))
        else:
            return render(request, "encyclopedia/edit_page.html", {
                "title": title,
                "form": page_form
            })
            
    
    entry = util.get_entry(title)
    page_form = EditPageForm({"content": entry})
    return render(request, "encyclopedia/edit_page.html", {
        "title": title,
        "form": page_form,
    })
    
def random_page(request):
    entries_list = util.list_entries()
    random_entry = random.choice(entries_list)
    return HttpResponseRedirect(reverse("page", args=[random_entry]))


