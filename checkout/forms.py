from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('full_name', 'email', 'phone_number',
                  'street_address1', 'street_address2',
                  'town_or_city', 'postcode', 'country',
                  'county',)
        
        # override init method allowing us to customize

        def __init__(self, *args, **kwargs):
            """
            Add placeholders and classes, remove auto-generated
            labels and set autofocus on first field
            """
            # call default init menthod to set form up as it would be by default
            super().__init__(*args, **kwargs)
            # set up placeholders in form fields instead of labels and empty textboxes
            placeholders = {
                'full_name': 'Full Name',
                'email': 'Email Address',
                'phone_number': 'Phone Number',
                'postcode': 'Postal Code',
                'town_or_city': 'Town or City',
                'street_address1': 'Street Address 1',
                'street_address2': 'Street Address 2',
                'county': 'County, State or Locality',
            }

            #set autofocus on full name so cursor starts in full name when page loads
            self.fields['full_name'].widget.attrs['autofocus'] = True
            # iterate through fields adding star to placeholder if it's required on the model
            for field in self.fields:
                if field != 'country':
                    if self.fields[field].required:
                        placeholder = f'{placeholders[field]} *'
                    else:
                        placeholder = placeholders[field]
                # set placeholder attributes to values in dictionary above
                self.fields[field].widget.attrs['placeholder'] = placeholder
                # add css class
                self.fields[field].widget.attrs['class'] = 'stripe-style-input'
                # remove form field labels
                self.fields[field].label = False

