from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('detsad/', views.DetsadListView.as_view(), name="detsad"),
    path('detsad/<int:pk>/', views.ChapterListView.as_view(), name="products"),
    path('detsad/<str:url_slug>/', views.SubcategoryListView.as_view(), name="products_of_sub"),
]