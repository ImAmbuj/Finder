from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    profile_pic = models.ImageField(upload_to = '')
    bio = models.TextField(max_length=150, blank=True)
    
    def __str__(self):
        return self.username

    def serialize(self):
     return {
        'id': self.id,
        "username": self.username,
        "profile_pic": self.profile_pic.url,
        "first_name" : self.first_name,
        "last_name" : self.last_name
        }   


class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    date_created = models.DateField(auto_now_add=True)
    post_text = models.TextField(max_length=130, blank=True)
    post_img = models.ImageField(upload_to= 'posts/', blank= True)
    likers = models.ManyToManyField(User, blank=True, related_name='likes')
    savers = models.ManyToManyField(User, blank=True,  related_name='savers')

    def __str__(self):
        return f"Post ID:{self.id}(creator: {self.creator})"    

    def img_url(self):
        return self.post_img.url 

    def append(self, name, value):
        self.name = value 



class Follower(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    followers = models.ManyToManyField(User,blank=True, related_name='following')

    def __str__(self):        
        return f"User : {self.user}"



