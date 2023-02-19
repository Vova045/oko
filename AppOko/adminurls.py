
from django.urls import path
from oko.settings import MEDIA_ROOT
from AppOko import views, AdminViews

urlpatterns = [
    path('admin/', views.adminLogin, name="admin_login"),
    path('admin_login_process', views.adminLoginProcess, name="admin_login_process"),
    path('admin_logout_process', views.adminLogoutProcess, name="admin_logout_process"),

    # Page for Admin
    path('admin_home', AdminViews.admin_home, name="admin_home"),

    # Categories
    path('chapter_list', AdminViews.ChaptersListView.as_view(), name="chapter_list"),
    path('chapter_create', AdminViews.ChaptersCreate.as_view(), name="chapter_create"),
    path('chapter_update/<slug:pk>', AdminViews.ChaptersUpdate.as_view(), name="chapter_update"),
    path('chapter_delete/<str:id>', AdminViews.ChapterDelete.as_view(), name="chapter_delete"),
    path('chapter_dublicate/<str:id>', AdminViews.ChapterDublicate.as_view(), name="chapter_dublicate"),


    # Subcategories
    path('sub_category_list', AdminViews.SubCategoriesListView.as_view(), name="sub_category_list"),
    path('sub_category_create', AdminViews.SubCategoriesCreate.as_view(), name="sub_category_create"),
    path('sub_category_update/<slug:pk>', AdminViews.SubCategoriesUpdate.as_view(), name="sub_category_update"),
    path('subcategory_delete/<str:id>', AdminViews.SubCategoryDelete.as_view(), name="subcategory_delete"),
    path('subcategory_dublicate/<str:id>', AdminViews.SubCategoryDublicate.as_view(), name="subcategory_dublicate"),

    # Categories
    path('category_list', AdminViews.CategoriesListView.as_view(), name="category_list"),
    path('category_create', AdminViews.CategoriesCreate.as_view(), name="category_create"),
    path('category_update/<slug:pk>', AdminViews.CategoriesUpdate.as_view(), name="category_update"),
    path('category_delete/<str:id>', AdminViews.CategoryDelete.as_view(), name="category_delete"),
    path('category_dublicate/<str:id>', AdminViews.CategoryDublicate.as_view(), name="category_dublicate"),


    #Products
    path('product_create', AdminViews.ProductView.as_view(),name="product_view"),
    path('product_list', AdminViews.ProductListView.as_view(),name="product_list"),
    path('product_edit/<str:product_id>', AdminViews.ProductEdit.as_view(),name="product_edit"),
    path('product_add_media/<str:product_id>', AdminViews.ProductAddMedia.as_view(),name="product_add_media"),
    path('product_edit_media/<str:product_id>', AdminViews.ProductEditMedia.as_view(),name="product_edit_media"),
    path('product_media_delete/<str:id>', AdminViews.ProductMediaDelete.as_view(),name="product_media_delete"),
    path('product_add_stocks/<str:product_id>', AdminViews.ProductAddStocks.as_view(),name="product_add_stocks"),
    path('file_upload', AdminViews.file_upload, name="file_upload"),
    path('product_delete/<str:id>', AdminViews.ProductDelete.as_view(),name="product_delete"),
    path('product_dublicate/<str:id>', AdminViews.ProductDublicate.as_view(),name="product_dublicate"),




    #Staff User
    path('staff_create',AdminViews.StaffUserCreateView.as_view(),name="staff_create"),
    path('staff_list',AdminViews.StaffUserListView.as_view(),name="staff_list"),
    path('staff_update/<slug:pk>',AdminViews.StaffUserUpdateView.as_view(),name="staff_update"),
    #Customer User
    path('customer_create',AdminViews.CustomerUserCreateView.as_view(),name="customer_create"),
    path('customer_list',AdminViews.CustomerUserListView.as_view(),name="customer_list"),
    path('customer_update/<slug:pk>',AdminViews.CustomerUserUpdateView.as_view(),name="customer_update"),
    path('customer_fast_create/',AdminViews.CustomerUserRandomCreateView.as_view(),name="customer_fast_create"),
    #TempCustomer User
    path('tempcustomer_create',AdminViews.TempCustomerUserCreateView.as_view(),name="tempcustomer_create"),
    path('tempcustomer_list',AdminViews.TempCustomerUserListView.as_view(),name="tempcustomer_list"),
    path('tempcustomer_update/<slug:pk>',AdminViews.TempCustomerUserUpdateView.as_view(),name="tempcustomer_update"),
    path('tempcustomer_fast_create/project=<str:id>',AdminViews.TempCustomerUserRandomCreateView.as_view(),name="tempcustomer_fast_create"),

    #Guests
    path('guest_list',AdminViews.GuestListView.as_view(),name="guest_list"),
    
    path('getdetails',AdminViews.ProductView.getdetails,name="getdetails"),
    path('getdetails2',AdminViews.ProductView.getdetails2,name="getdetails2"),
    path('getdetails_for_sub_category_create',AdminViews.SubCategoriesCreate.getdetails_for_sub_category_create,name="getdetails_for_sub_category_create"),
    path('getdetails_for_category_gallery_create',AdminViews.CategoryGalleryCreate.getdetails_for_category_gallery_create,name="getdetails_for_category_gallery_create"),

    #Gallery
    path('gallery_create',AdminViews.GalleryCreate.as_view(),name="gallery_create"),
    path('gallery_update/<str:id>',AdminViews.GalleryUpdate.as_view(),name="gallery_update"),
    path('gallery_delete/<str:id>',AdminViews.GalleryDelete.as_view(),name="gallery_delete"),
    path('gallery_dublicate/<str:id>',AdminViews.GalleryDublicate.as_view(),name="gallery_dublicate"),
    path('gallery_list',AdminViews.GalleryListView.as_view(),name="gallery_list"),
    path('category_for_gallery_create',AdminViews.CategoryGalleryCreate.as_view(),name="category_for_gallery_create"),
    path('category_for_gallery_delete/<str:id>',AdminViews.CategoryGalleryDelete.as_view(),name="category_for_gallery_delete"),
    path('projects_list',AdminViews.ProjectListView.as_view(),name="projects_list"),
]
