from django.shortcuts import render
from django.http import HttpResponse
from .models import Blogs
def index(request):
    
    return render(request, 'rango/index.html')

def login(request):

    return render(request, 'rango/login.html')

def register(request):

    return render(request, 'rango/register.html')

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



class BlogCreateView(View):
    def get(self, request):
        form = BlogForm()
        return render(request, 'rango/upload.html', {'form': form})

    def post(self, request):
        form = BlogForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            # 临时创建一个用户，绑定到博客上
            #user = User.objects.create_user('temporary_user')
            #blog.user_id = user.id
            #finish login code:
            blog = form.save(commit=False)
            blog.user_id = request.user
            #default_user, created = User.objects.get_or_create(username='default_user') fake user code
            #blog.user = default_user
            #blog.save()
            return redirect('../blogs')
        return render(request, 'rango/upload.html', {'form': form})

#@login_required
#class BlogCreateView(request): #create the blogs
#   model = Blog#the model type
#   form_class = BlogForm # using form
#   template_name = 'upload.html' #the html file
#   success_url = reverse_lazy('blogs')#提交后的重定向页面

#def form_valid(self, form):#提交表单后该方法被调用，用于处理表单数据
#        form.instance.user_id = self.request.user_id
#        return super().form_valid(form)

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Post
from .models import PostForm

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
