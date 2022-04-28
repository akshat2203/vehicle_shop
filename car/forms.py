from django import forms
from django.forms import fields

from .models import User, Car
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']


class AddCarForm(forms.ModelForm):
    year = fields.DateField(widget=forms.widgets.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Car
        fields = ['modal', 'make', 'condition', 'price', 'description', 'year']

    def clean(self):
        cleaned_data = super(AddCarForm, self).clean()
        price = int(cleaned_data.get("price"))

        if price not in range(1000, 100001):
            self.add_error('price', 'Enter valid price')

        return cleaned_data
