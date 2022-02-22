from django.apps import apps
from django.contrib import admin
from server.jornal_app.models.admin import UserAdmin

from server.jornal_app.models.users import User


def autoregister(*app_list : str) -> None: 
    """
    register all database models in the admin dashboard
    """
    for app in app_list :
        for model_name, model in apps.get_app_config(app).models.items() :
            if '_' not in model_name   :
                if globals().get(model.__name__+'Admin')   :
                    admin.site.register(model, globals().get(model.__name__+'Admin'))
                else :
                    if model == 'User' : 
                        admin.site.register(User,UserAdmin)
                    else:
                        admin.site.register(model)


admin.site.site_header, 
admin.site.site_title, 
admin.site.index_title = "Jornal administration"

autoregister('jornal_app')