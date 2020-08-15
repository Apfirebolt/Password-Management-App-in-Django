from django.urls import re_path
from password_manager import settings
from django.conf.urls.static import static
from . views import AccountsHome, create_user, login_user, logout_view

urlpatterns = [
    re_path(r'^$', AccountsHome.as_view(), name='home'),
    re_path(r'^register$', create_user, name='register'),
    re_path(r'^login$', login_user, name='login'),
    re_path(r'^logout$', logout_view, name='logout')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
