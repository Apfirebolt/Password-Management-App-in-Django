from django.urls import re_path, path
from password_manager import settings
from django.conf.urls.static import static
from . views import ( create_category, password_home, create_password, detail_password, update_hints, update_password,
                      delete_password, create_generated_password, update_generated_password, delete_generated_password,
                      list_generated_password, file_delete_view, file_detail_view, file_list, upload_file,
                      )

urlpatterns = [
    re_path(r'^$', password_home, name='home'),
    re_path(r'^create_category$', create_category, name='create_category'),
    re_path(r'^create_password$', create_password, name='create_password'),
    path('detail/<int:pk>', detail_password, name='detail_password'),
    path('update_hints/<int:pk>', update_hints, name='update_hints'),
    path('update_password/<int:pk>', update_password, name='update_password'),
    path('delete_password/<int:pk>', delete_password, name='delete_password'),
    re_path(r'^create_generated_password$', create_generated_password, name='create_generated_password'),
    path('update_generated_password/<int:pk>', update_generated_password, name='update_generated_password'),
    path('delete_generated_password/<int:pk>', delete_generated_password, name='delete_generated_password'),
    re_path(r'^generated_passwords$', list_generated_password, name='generated_passwords'),
    re_path(r'^upload_file$', upload_file, name='upload_file'),
    re_path(r'^file_list', file_list, name='file_list'),
    path('file_detail/<int:pk>', file_detail_view, name='file_detail'),
    path('file_delete/<int:pk>', file_delete_view, name='file_delete'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
