
from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('', home, name="home"),
    path('home/', home, name="home"),
    path('login', loginpage, name="login"),
    path('updateProject/<int:pk>/', update_project, name="update_project"),
    path('createProject/', create_project, name="update_project"),
    path('deleteProject/<int:pk>/', delete_project, name = "delete_project"),
    path('logout/', logoutUser, name="logout"),
    path('signup/', signup, name="signup")

]
from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)