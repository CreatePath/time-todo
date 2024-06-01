from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    """
    AbstractUser를 상속받아 만들어진 timetodo의 User class
    Django에서 제공하는 authentication 기능 사용 가능
    
    password: user의 비밀번호
    message: user의 상태메세지
    """
    password = models.CharField(max_length=64)
    message = models.TextField(max_length=100)

    def __str__(self):
        return self.get_username()