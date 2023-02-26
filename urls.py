from django.urls import path

from django.conf.urls.static import static
from oko import settings
from django.urls import include
from AppOko import views

urlpatterns = [
    path('', include('AppOko.mainurls')),
    path('admindashboard/', include("AppOko.adminurls")),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)+static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
