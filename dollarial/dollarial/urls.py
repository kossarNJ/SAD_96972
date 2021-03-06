from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('user_management.urls')),
    path('admin_panel/', include('admin_panel.urls')),
    path('user_panel/', include('user_panel.urls')),
    path('', include('website.urls')),
]
