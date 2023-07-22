from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


admin.site.site_header  =  "Admin Panel - YourFriendd"  
admin.site.site_title  =  "Admin Panel - YourFriendd"
admin.site.index_title  =  "YourFriendd"

schema_view = get_schema_view(
    openapi.Info(
        title="YourFriendd API",
        default_version='v1',
        description="YourFriendd"
    ),
    public=True
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('authentication.urls')),
    path('api/', include('consultation.urls')),
    path('api/', include('home.urls')),

    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)