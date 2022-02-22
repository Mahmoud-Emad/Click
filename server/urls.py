from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from server.jornal_app.utils.auth import MyTokenRefreshView
from server.jornal_app.views.auth import PasswordResetAPIView, UserLoginApiView, UserRegisternIfoAPIView, login_view
from server.jornal_app.views.lobby import home_page

urlpatterns = [
    path('',home_page, name = "home"),
    path('login/', login_view, name = 'login'),
    path('admin/', admin.site.urls),
    path('api/', include([
        path('auth/', include([
            path('sign-in/', UserLoginApiView.as_view()),
            path('sign-up/', UserRegisternIfoAPIView.as_view()),
            path('token/refresh/', MyTokenRefreshView.as_view()),
            path('reset-password/', PasswordResetAPIView.as_view()),
        ])),

        # users endpoints
        path('users/', include('server.jornal_app.routers.users')),
        
        # friends endpoint
        path('friends/', include('server.jornal_app.routers.friends')),
        
        # posts endpoints
        path('posts/', include('server.jornal_app.routers.posts')),
        
        # lobby endpoints
        path('lobby/', include('server.jornal_app.routers.lobby')),
        
        # pages endpoints
        path('pages/', include('server.jornal_app.routers.pages')),
        
        # Real Time endpoints 
        path('messanger/', include('server.jornal_app.routers.real_time_url')),
]))
]


if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static
    from drf_yasg.views import get_schema_view
    from drf_yasg import openapi

    schema_view = get_schema_view(
        openapi.Info(
            title="Api Documentation",
            default_version='v1',
        ),
        public=False,
    )

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),
        # Swagger
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

        # noqa: DJ05
    ] + urlpatterns + static(  # type: ignore
        # Serving media files in development only:
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )

