from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import Book



class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)




class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'cover_image']
 
#userrrrrrrrrrrrrrrrrr       


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


