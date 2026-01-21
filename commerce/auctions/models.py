from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Auction')
    
class Category(models.Model):
    category_name = models.CharField(max_length=24)

class Auction(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_auctions")
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    starting_bid = models.DecimalField(max_digits=8, decimal_places=2)
    is_active = models.BooleanField(default=True)
    won_by = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True, related_name="auctions_won")
    img_url = models.URLField(blank=True, null=True) # optional
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, default=None, null=True, related_name="category") # optional


    
class Bid(models.Model):
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="biddings")
    bid_price = models.DecimalField(max_digits=8, decimal_places=2)
    bid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidding")
    
class Comment(models.Model):
    comment_text = models.CharField(max_length=255)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments")
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments")
    

    
    
