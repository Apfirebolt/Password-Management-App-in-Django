from django.urls import re_path, path
from password_manager import settings
from django.conf.urls.static import static
from . views import create_category, password_home, create_password, detail_password, update_hints, update_password, delete_password

urlpatterns = [
    re_path(r'^$', password_home, name='home'),
    re_path(r'^create_category$', create_category, name='create_category'),
    re_path(r'^create_password$', create_password, name='create_password'),
    path('detail/<int:pk>', detail_password, name='detail_password'),
    path('update_hints/<int:pk>', update_hints, name='update_hints'),
    path('update_password/<int:pk>', update_password, name='update_password'),
    path('delete_password/<int:pk>', delete_password, name='delete_password'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
