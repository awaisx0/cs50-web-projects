from django import forms


from .models import User, Auction, Bid, Comment, Category


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", max_length=64)
    description = forms.CharField(label="Description", widget=forms.Textarea, max_length=500)
    bid_price = forms.DecimalField(label="Starting bid price", max_digits=8, decimal_places=2)
    img_url = forms.URLField(label="Image URL for the listing", required=False)
    category = forms.ChoiceField(choices=[], required=False)
    
    # cs50 help in overriding the init method
    def __init__(self, *args, **kwargs):
        super(NewListingForm, self).__init__(*args, **kwargs)
        self.fields['category'].choices = [('', 'Select a category')] + [(obj.id, obj.category_name) for obj in Category.objects.all()]
    
    
class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="Your bid is the current bid", max_digits=8, decimal_places=2)
    
    # cs50.ai gave this validation code
    def __init__(self, *args, **kwargs):
        self.min_bid = kwargs.pop('min_bid', None)
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        bid = cleaned_data.get('bid')
        
        # valid bid price
        if bid <= self.min_bid:
            raise forms.ValidationError(f"Bid must be at least greater than current max bid: {self.min_bid}")
    
class NewCommentForm(forms.Form):
    comment_text = forms.CharField(label="Comment", max_length=500)