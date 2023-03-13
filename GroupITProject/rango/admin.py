from django.contrib import admin



from .models import Blogs
from .models import User
admin.site.register(Blogs)
admin.site.register(User)
# Register your models here.


