from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.conf import settings

# Create your models here.

class CustomUserManager(BaseUserManager):
    # Custom manager for handling user creation and management
    def create_user(self, email, username, password=None):
        # Method for creating a regular user
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        # Method for creating a superuser
        user = self.create_user(email=email, username=username, password=password)
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name ="emailaddress", max_length=200, unique=True)
    username = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username

class Books(models.Model):
    book_name = models.CharField(max_length=50)
    quantity = models.PositiveIntegerField(default=0)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.book_name

class Borrow(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    due_date = models.DateField()
    borrowed_date = models.DateField(auto_now_add=True)
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.book_name} - Borrowed by {self.user.username}"


class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    borrowed_books = models.ManyToManyField(Books, blank=True, related_name='borrowed_by')
    favourite_books = models.ManyToManyField(Books, blank=True, related_name='favourited_by')

    def __str__(self):
        return self.user.username
