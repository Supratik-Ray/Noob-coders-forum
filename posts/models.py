from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

# Create your models here.
class Post(models.Model):
    POST_TYPE_CHOICES = (
        ('doubt', 'Doubt/Question'),
        ('learning', 'Learning'),
        ('resource', 'Resource'),
    )
    title = models.CharField(max_length=255)
    # body = models.TextField()
    body = RichTextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    likes = models.ManyToManyField(User,related_name='liked_post',blank=True)
    post_type = models.CharField(max_length=20,choices=POST_TYPE_CHOICES,default='learning')

    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    text = RichTextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.title}"
    
    