from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogs
from django.contrib import messages
from rango.forms import UserForm
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.views.generic import View
from .forms import BlogForm
#from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
def index(request):
    
    return render(request, 'rango/index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:

                auth_login(request, user)
                return redirect(reverse('rango:index'))
            else:
                messages.info(request, 'Your account is disabled.')
                return render(request, 'rango/login.html')
        else:
            messages.info(request, 'Invalid login details supplied.')
            return render(request, 'rango/login.html')
    else: 
        return render(request, 'rango/login.html')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.username = user.username.lower()
            user.set_password(user.password)
            user.save()
            login(request, user)
            return redirect('index')
                
        else:
            messages.error(request, 'An error occurred during registration')
    else:
        user_form = UserForm()

    return render(request,
            'rango/register.html',
            {'user_form': user_form} )
            
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


def upload(request):

    return render(request, 'rango/upload.html')

def blogs(request):

    return render(request, 'rango/blogs.html')

def UserProfile(request):

    return render(request, 'rango/UserProfile.html')

def admin(request):

    return render(request, 'rango/admin.html')


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'rango/blogs.html', {'posts': posts})

#@login_required
def blog_list(request):#show the blogs
    blogs = Blogs.objects.all()# select all blog object from database
    return render(request, 'rango/blogs.html', {'blogs': blogs})


@login_required
class BlogCreateView(View):
    def get(self, request):
        form = BlogForm()
        return render(request, 'rango/upload.html', {'form': form})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            # ?????????????????????????????????????????????
            #user = User.objects.create_user('temporary_user')
            #blog.user_id = user.id
            #finish login code:
            blog = form.save(commit=False)
            #user = User.objects.get(id=request.user.id)
            blog = Blogs(title=title, content=content, user_id=user)
            blog.user_id = request.user
            #default_user, created = User.objects.get_or_create(username='default_user') fake user code
            #blog.user = default_user
            #blog.save()
            return redirect('../blogs')
        return render(request, 'rango/upload.html', {'form': form})
@login_required
def submit_blog(request):
    user_instance = request.user
    if request.method == 'POST':
        #form = BlogForm(request.POST, request.FILES)
        #user_instance = get_user_model().objects.get(id=request.user.id)
        #user_instance = request.user
        #user_instance = User.objects.get(email=request.user.email)
        user_id = request.session.get('user_id')
        blog_headline = request.POST['blog_headline']
        restaurant_name = request.POST['restaurant_name']
        rating = request.POST['rating']
        location = request.POST['location']
        #user_id = user_instance.id
        review = request.POST['review']

        blog = Blogs(blog_headline=blog_headline, restaurant_name=restaurant_name, rating=rating,location=location,review=review,user_id=user_id)

        blog.save()
        return redirect('../blogs')
    return render(request, 'rango/upload.html')


 #fields = ['blog_headline','restaurant_name' ,'rating','location','user_id', 'review']








#@login_required
#class BlogCreateView(request): #create the blogs
#   model = Blog#the model type
#   form_class = BlogForm # using form
#   template_name = 'upload.html' #the html file
#   success_url = reverse_lazy('blogs')#???????????????????????????

#def form_valid(self, form):#????????????????????????????????????????????????????????????
#        form.instance.user_id = self.request.user_id
#        return super().form_valid(form)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Post
from .forms import PostForm

# Administrator Login View Functions
def admin_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            error = 'Invalid username or password'
    else:
        error = ''
    return render(request, 'admin/login.html', {'error': error})

# Article List View Functions
@login_required(login_url='admin_login')
def dashboard(request):
    posts = Post.objects.all()
    return render(request, 'admin/dashboard.html', {'posts': posts})

# New article view function
@login_required(login_url='admin_login')
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = PostForm()
    return render(request, 'admin/new_post.html', {'form': form})

@login_required
def delete_blog(request, blogs_id):
    blogs = get_object_or_404(Blogs, pk=blog_id)
    if request.user == blogs.user_id:
        blogs.delete()
        return redirect('blog_list')
    else:
        raise Http404
 
def blog_search(request):
    query = request.GET.get('q')
    order_by = request.GET.get('order_by', '-rating')  # The default is in descending order
    if order_by == 'rating':
        results = Blogs.objects.filter(title__icontains=query).order_by('rating')
    else:
        results = Blogs.objects.filter(title__icontains=query).order_by('-rating')
    return render(request, 'blog_search.html', {'results': results, 'order_by': order_by})
