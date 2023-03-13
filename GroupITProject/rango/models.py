from django.db import models


# Create your models here.
class User(models.Model):
    # This file will be uploaded to MEDIA_ROOT /the user(id)/thefile
    User_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=128,unique=True)
    last_name = models.CharField(max_length=128,unique=True)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return str(self.User_id)


class Blogs(models.Model):
    Blog_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    restaurant_name = models.CharField(max_length=128)
    rating = models.FloatField()
    location = models.CharField(max_length=128)
    blog_headline = models.CharField(max_length=20)
    review = models.TextField(max_length=1500)
    likes_count = models.IntegerField(default=0)
    comments_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.Blog_id)


class Comment(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    blog_id = models.ForeignKey(Blogs,on_delete=models.CASCADE)
    comment = models.TextField(max_length=1500)

    def __str__(self):
        return str(self.comment)

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title





