from django.db import models
from server.jornal_app.models.abstracts import TimeStampedModel
from server.jornal_app.models.posts import Post

from server.jornal_app.models.users import User

def Get_progile_image_file_path(self, filename):
    """Handel user media files"""
    return f'server/media/pages/{self.pk}/profile_images/{self.modified}{filename[filename.index("."):]}'

def Get_progile_cover_file_path(self, filename):
    """Handel user media files"""
    return f'server/media/pages/{self.pk}/progile_covers/{self.modified}{filename[filename.index("."):]}'

class USERTYPE(models.TextChoices):
    ADMIN       = "ADMIN", "ADMIN"
    EDITOR      = "EDITOR", "EDITOR"
    AUTHOR      = "AUTHOR", "AUTHOR"

class Category(models.Model):
    name = models.CharField(max_length = 100, unique=True)
    
    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.name)

class Permissions(TimeStampedModel):
    permission = models.CharField(max_length=50)
    user_type = models.CharField(max_length=50, choices=USERTYPE.choices)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.permission)

class PageUserPermission(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=50, choices=USERTYPE.choices)
    permissions = models.ManyToManyField(Permissions, related_name='user_page_per')
    pages = models.ManyToManyField('UserPage', related_name="user_pages", null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return f'{self.user_type}-{self.user.email.upper()}'

class UserPage(TimeStampedModel):
    page_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100, null=True, blank=True)
    users = models.ManyToManyField(PageUserPermission, related_name='users')
    about = models.TextField(max_length=500)
    category = models.ManyToManyField(Category, related_name="cats")
    profile_image = models.ImageField(upload_to = Get_progile_image_file_path) 
    profile_cover = models.ImageField(upload_to = Get_progile_cover_file_path)
    followers   = models.ManyToManyField(User,related_name='page_followers')
    is_active = models.BooleanField(default=False)
    posts   = models.ManyToManyField(Post,related_name='page_posts')

    def __str__(self) -> isinstance:
        """Return string of instance"""
        return str(self.page_name)