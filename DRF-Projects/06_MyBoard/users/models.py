from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
# one-to-one relationship with User model(Profile model)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
        # primary_key를 User의 pk로 설정
    nickname = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    subjects = models.CharField(max_length=100)
    image = models.ImageField(upload_to='profile/', default='default.png') # 경로와 이미지 기본값 설정

@receiver(post_save, sender=User) # User모델이 post_save 이벤트 발생시키면 create_user_profile 함수 실행
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)