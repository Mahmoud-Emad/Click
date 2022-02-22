from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserChangeForm

from server.jornal_app.models.users import User


class MyUserChangeForm(UserChangeForm):
    """
    handle the admin dashboard list fields
    """
    class Meta(UserChangeForm.Meta):
        model = User

class UserAdmin(BaseUserAdmin):
    form = MyUserChangeForm
    list_display = ('id', 'email','full_name', 'date_joined', 'is_admin', 'is_active', 'is_staff', 'is_superuser')
    
    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'is_admin', 'is_active', 'is_staff', 'is_superuser','groups')}),
    )
