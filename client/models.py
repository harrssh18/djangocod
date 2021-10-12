from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
	email = models.EmailField(unique=True)
	height = models.FloatField()
	weight = models.FloatField()
	age = models.IntegerField()
	plan_days = models.IntegerField()

	objects = UserManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []  
   