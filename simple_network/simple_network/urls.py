from django.contrib import admin
from django.urls import path

from account.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
]