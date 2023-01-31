from django.urls import path
from . import views
from .decorators import check_recaptcha


urlpatterns = [
    path('', check_recaptcha(views.home), name='home'),
    path('bukvy/', check_recaptcha(views.bukvy), name='bukvy'),
    path('detsad/', views.DetsadListView.as_view(), name="detsad"),
    path('detsad/<int:pk>/', views.ChapterListView.as_view(), name="products"),
    path('detsad/<str:url_slug>/', views.SubcategoryListView.as_view(), name="products_of_sub"),
]