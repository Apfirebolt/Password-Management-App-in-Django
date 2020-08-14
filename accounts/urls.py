from django.urls import re_path
from password_manager import settings
from django.conf.urls.static import static
from . views import AccountsHome

urlpatterns = [
    re_path(r'^$', AccountsHome.as_view(), name='home')

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
