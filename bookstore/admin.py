from django.contrib import admin

from .models import CustomUser,Books, Borrow,UserProfile

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Books)
admin.site.register(Borrow)
admin.site.register(UserProfile)
