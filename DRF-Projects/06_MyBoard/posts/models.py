from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from users.models import Profile

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts') # related_name='posts' is used to access the posts of a user
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    body = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.png')
    likes = models.ManyToManyField(User)
    published_date = models.DateTimeField(default=timezone.now)