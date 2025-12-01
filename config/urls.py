from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Redirect root to classes list
    path('', RedirectView.as_view(url='/classes/', permanent=False), name='home'),
    
    # App URLs
    path('accounts/', include('accounts.urls')),
    path('classes/', include('core.urls')),
    
    # API URLs
    path('api/', include('api_gateway.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Customize admin site
admin.site.site_header = "Class Manager Administration"
admin.site.site_title = "Class Manager Admin"
admin.site.index_title = "Welcome to Class Manager Admin Panel"