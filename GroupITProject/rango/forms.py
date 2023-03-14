from django import forms
from .models import Blogs
from django.contrib.auth.models import User 


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blogs
        fields = ['blog_headline','restaurant_name' ,'rating','location','author', 'review']

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class UserForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='password2', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email','password','password2']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        # Check if both password fields are filled out
        if not password:
            self.add_error('password', 'Password is required')
        if not password2:
            self.add_error('password2', 'Confirm Password is required')

        # Check if both passwords match
        if password and password2 and password != password2:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

