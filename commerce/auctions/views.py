from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms


from .models import User, Auction, Bid, Comment

class NewListingForm(forms.Form):
    title = forms.CharField(label="Title" ,max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea)
    bid_price = forms.DecimalField(label="Starting bid price", max_digits=8, decimal_places=2)
    img_url = forms.URLField(label="Image URL for the listing", required=False)
    category = forms.CharField(max_length=25, label="Category", required=False)
    


def index(request):
    listings = Auction.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
    
    
    
def create_new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid_price = form.cleaned_data["bid_price"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]
            new_auction = Auction(owner=request.user, title=title, description=description, starting_bid=bid_price, img_url=img_url, category=category)
            new_auction.save()
            
            return HttpResponseRedirect(reverse("index"))
            
            
            
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
            
            
    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })


def listing_view(request, listing_id):
    auction = Auction.objects.filter(id = listing_id).first()
    return render(request, "auctions/listing.html", {
        "auction": auction
    })