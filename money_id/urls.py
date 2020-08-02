from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views

app_name = "money_id" 

urlpatterns = [
    path("",views.index,name="home"),
    path("detected/",views.main,name="detect"),
    path("capture/",views.capture,name="capture"),
    path("upload/",views.uploader,name="upload"),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)