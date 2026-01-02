from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from ckeditor.fields import RichTextField

# Define Category model FIRST
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='avatars/default.png')
    
    def __str__(self):
        return f'{self.user.username} Profile'

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()  # Changed from TextField to RichTextField
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  # Now Category is defined
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.title

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['post', 'user']  # Prevent duplicate likes

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_date']
    
    def __str__(self):
        return f'Comment by {self.author} on {self.post}'