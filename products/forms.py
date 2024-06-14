from django import forms
from .models import Product, Category

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    # override __init__ method to make changes to fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        # get friendly name
        friendly_names = [{c.id, c.get_friendly_name()} for c in categories]

        # update category field to show friendly name instead of id
        self.fields['category'].choices = friendly_names
        # Iterate through the rest of these fields and set some classes on 
        # them to make them match the theme of the rest of the store.
        for fiels_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'