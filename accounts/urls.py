from django.urls import re_path
from password_manager import settings
from django.conf.urls.static import static
from . views import ( AccountsHome, create_user, login_user, logout_view,
                    update_password, update_profile_image, update_settings )

urlpatterns = [
    re_path(r'^$', AccountsHome.as_view(), name='home'),
    re_path(r'^register$', create_user, name='register'),
    re_path(r'^login$', login_user, name='login'),
    re_path(r'^logout$', logout_view, name='logout'),
    re_path(r'^update_password$', update_password, name='update_password'),
    re_path(r'^update_image$', update_profile_image, name='update_profile_image'),
    re_path(r'^update_settings$', update_settings, name='update_settings')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
