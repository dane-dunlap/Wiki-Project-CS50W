from django.shortcuts import render
from django.http import HttpResponse
from markdown2 import Markdown

from . import util

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
    entry = util.get_entry(title)
    if entry == None:
        return render(request,"encyclopedia/error.html")
    
    return render(request,"encyclopedia/entry.html", {
        "content":markdowner.convert(entry),"title":title
    })

def search(request):
    if request.method == "GET":
        title = request.GET['q']
        entry = util.get_entry(title)
        if entry == None:
            all_entries = util.list_entries()
            search_results = []
            for entry in all_entries:
                if title in entry:
                    search_results.append(entry)
            if search_results:
                return render(request,"encyclopedia/search_results.html",{
                "search_results":search_results
            })
            else:
                return render(request,"encyclopedia/no_search.html")
        
        return render(request,"encyclopedia/entry.html", {
        "content":markdowner.convert(entry),"title":title
    })

def create(request):
    if request.method =="GET":
        return render(request,"encyclopedia/create.html")

    if request.method == "POST":
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title,content)
        new_entry = util.get_entry(title)
        
        return render(request,"encyclopedia/entry.html", {
        "content":markdowner.convert(new_entry),"title":title
    })
