from random import randint
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

#This fuction Creates Users 
class UserManager(BaseUserManager):
    """
    Custom manager for the User model.
    """
    def create_user(self, email, password=None, **extra_fields): 
        """
        Creates and returns a regular user with an email and password.
        """
        if not email:
            raise ValueError("Users Must Have an Email Address")
        
        email = self.normalize_email(email)
        
        
        user = self.model(email = email, **extra_fields)
        user.set_password(password)
        
        
        user.save(using = self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):  
        """
        Creates and returns a superuser with an email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password= None, **extra_fields) #
    
class User(AbstractBaseUser, PermissionsMixin):
    
    """
    Custom user model with email as the unique identifier.
    """
    email = models.EmailField(unique=True)
    
    
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    date_joined = models.DateField(auto_now_add=True)
    
    objects = UserManager() 
    
    USERNAME_FIELD = 'email'
    
        
    def get_full_name(self):
        return self.first_name + " " + self.last_name
        
        
    def __str__(self) -> str:
        return self.email
    
    
        