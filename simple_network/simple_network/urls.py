from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from account.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('profile/<int:id>/', profile_view, name='profile'),
    path('settings/', settings_view, name='settings'),
    path('post/new', add_post_view, name='add_post'),
    path('post/delete/<int:post_id>', delete_post_view, name='delete_post'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()