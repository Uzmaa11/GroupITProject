from django import forms
from .models import Blogs

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

