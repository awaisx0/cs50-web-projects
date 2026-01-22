from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


from .models import User, Auction, Bid, Comment, Category
from .forms import NewListingForm, NewBidForm, NewCommentForm
    


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
    
    
# CREATE NEW LISTING VIEW
    
@login_required
def create_new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            bid_price = form.cleaned_data["bid_price"]
            img_url = form.cleaned_data["img_url"]
            category = form.cleaned_data["category"]
            category_obj = None
            if category:
                category_obj = Category.objects.filter(category_name=category).first()
            new_auction = Auction(owner=request.user, title=title, description=description, starting_bid=bid_price, img_url=img_url, category=category_obj)
            new_auction.save()
            
            # redirect back to index
            return HttpResponseRedirect(reverse("index"))
            
            
        # if form data is not valid, re-render template with populated form to show user errors
        else:
            return render(request, "auctions/create_listing.html", {
                "form": form
            })
            
    
    # GET request rendering with new form
    return render(request, "auctions/create_listing.html", {
        "form": NewListingForm()
    })


def listing_view(request, listing_id):
    # get auction listing
    auction = Auction.objects.filter(id = listing_id).first()
    # get comments
    comments = Comment.objects.filter(auction=auction)
    # bids count so far
    bids_count = len(Bid.objects.filter(auction=auction))
    
    # initial price of auction
    current_price = auction.starting_bid
    # if more than 0 bids exist, get the bid_price of the highest bid
    if bids_count > 0:
        current_price = Bid.objects.filter(auction=auction).order_by("-bid_price").first().bid_price
        
        
    added_watchlist = False
    # get all users which have item on watchlist
    watchers = auction.watchers.all()
    # if current user is a watcher
    if request.user in watchers:
        added_watchlist = True
        
        
    # User Ownership
    is_owner = False
    owner = auction.owner
    # if current user matches owner object of auction, current user is the owner
    if request.user == owner:
        is_owner = True
    
    
    # rendering listing template
    return render(request, "auctions/listing.html", {
        "is_owner":  is_owner,
        "auction": auction,
        "bids_count": bids_count,
        "bid_price": current_price,
        "bidForm": NewBidForm(),
        "added_watchlist": added_watchlist,
        "commentForm": NewCommentForm(),
        "comments": comments,
    })



# BID VIEW
@login_required
def bid_view(request, listing_id):
    auction = Auction.objects.get(pk=listing_id)
    bids_on_listing = Bid.objects.filter(auction=auction)
    
    initial_bid_price = auction.starting_bid
    min_bid = initial_bid_price
    if len(bids_on_listing) > 0:
        listings_max_bid = bids_on_listing.order_by("-bid_price").first().bid_price
        min_bid = listings_max_bid
    
    bidder_id = request.user.id
    bidder = User.objects.get(pk=bidder_id)
    
    
    if request.method == "POST":
        bid_form = NewBidForm(request.POST, min_bid=min_bid)
        
        if bid_form.is_valid():
            bid_price = bid_form.cleaned_data['bid']

            # creating new bid and saving
            new_bid = Bid(bid_price=bid_price, bid_by=bidder, auction=auction)
            new_bid.save()

            # upon success redirect to listing view
            return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))
        
        else:
            auction = Auction.objects.filter(id = listing_id).first()
            return render(request, "auctions/listing.html", {
                "auction": auction,
                "bidForm": bid_form
            })
            
                
                
def comment_view(request, listing_id):
    if request.method == "POST":
        new_comment_form = NewCommentForm(request.POST)
        
        if new_comment_form.is_valid():
            comment_text = new_comment_form.cleaned_data.get("comment_text")
            user_id = request.POST.get("user_id")
            
            user = User.objects.get(pk=user_id)
            auction = Auction.objects.get(pk=listing_id)

            new_comment = Comment(comment_text=comment_text, auction=auction, comment_by=user)

            new_comment.save()
            return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))

        
# ADD TO WATCHLIST VIEW
@login_required
def add_watchlist(request, listing_id):
    auction = Auction.objects.get(pk=listing_id)
    user = User.objects.get(pk=request.user.id)
    user.watchlist.add(auction)
    return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))

# WATCHLIST view
def watchlist(request):
    user = User.objects.get(pk=request.user.id)
    watch_auctions = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist": watch_auctions,
    })
    
    
# REMOVE FROM WATCHLIST VIEW
@login_required
def remove_watchlist(request, listing_id):
    # get auction to remove
    auction = Auction.objects.get(pk=listing_id)
    # get current user
    user = User.objects.get(pk=request.user.id)
    # remove auction from user watchlist
    user.watchlist.remove(auction)
    return HttpResponseRedirect(reverse("listing_view", args=[listing_id]))

@login_required
def close_auction(request, listing_id):
    # get auction
    auction = Auction.objects.get(pk=listing_id)
    # get highest bidder
    highest_bidder = Bid.objects.filter(auction=auction).order_by("-bid_price").first().bid_by
    # get auction owner
    owner = auction.owner
    
    # if owner is the user, "close" the auction
    if request.user == owner:
        # set winner
        auction.won_by = highest_bidder
        # close
        auction.is_active = False
        auction.save()
        
        return HttpResponseRedirect(reverse(closed_listing_view, args=[listing_id]))
        
        
    
    return HttpResponseRedirect(reverse(listing_view, args=[listing_id]))

def closed_listing_view(request, listing_id):
    # get auction listing
    auction = Auction.objects.filter(id = listing_id).first()
    # get comments
    comments = Comment.objects.filter(auction=auction)
    # bids count so far
    bids_count = len(Bid.objects.filter(auction=auction))
    
    # initial price of auction
    current_price = auction.starting_bid
    # if more than 0 bids exist, get the bid_price of the highest bid
    if bids_count > 0:
        current_price = Bid.objects.filter(auction=auction).order_by("-bid_price").first().bid_price
        
        
    added_watchlist = False
    # get all users which have item on watchlist
    watchers = auction.watchers.all()
    # if current user is a watcher
    if request.user in watchers:
        added_watchlist = True
        
        
    # User Ownership
    is_owner = False
    owner = auction.owner
    # if current user matches owner object of auction, current user is the owner
    if request.user == owner:
        is_owner = True
        
    # Winner
    is_winner = False
    winner = auction.won_by
    if request.user == winner:
        is_winner = True
    
    
    # rendering closed listing template
    return render(request, "auctions/closed_listing.html", {
        "is_owner":  is_owner,
        "is_winner": is_winner,
        "auction": auction,
        "bids_count": bids_count,
        "bid_price": current_price,
        "added_watchlist": added_watchlist,
        "commentForm": NewCommentForm(),
        "comments": comments,
    })


def categories(request):
    all_categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": all_categories,
    })