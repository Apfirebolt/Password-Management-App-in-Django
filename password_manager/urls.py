from django.contrib import admin
from django.urls import path, include
from password_manager import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from . views import bad_request, no_permissions, not_found, server_error

urlpatterns = [
    path('', TemplateView.as_view(template_name='homepage.html'), name='home'),
    path('admin/', admin.site.urls),
    path('accounts/', include(('accounts.urls', 'accounts'), namespace='accounts')),
    path('passwords/', include(('passwords.urls', 'passwords'), namespace='passwords')),
]

urlpatterns += static(settings.MEDIA_URL, dcument_root=settings.MEDIA_ROOT)

handler400 = bad_request
handler403 = no_permissions
handler404 = not_found
