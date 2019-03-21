from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('vehicles/', include('django.contrib.auth.urls'), name='login'),
    path('vehicles/', include('django.contrib.auth.urls'), name='logout'),
]
urlpatterns += [
    path('vehicles/', include('vehicles.urls')),
    path('settings/', include('settings.urls')),
]

# Use static() to add url mapping to serve static files during development (only)
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='/vehicles/')),
]
