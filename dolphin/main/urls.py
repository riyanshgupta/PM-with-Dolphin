
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('/home', home, name="home"),
    path('/login', loginpage, name="login"),
    path('/updateRoom/<int: pk>', update_project, name="update_project"),
    path('/creatRoom', create_project, name="update_project"),
    path('/deleteProject/<int: pk>', delete_project, name = "delete_project"),

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)