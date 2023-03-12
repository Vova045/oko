from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, CreateView, UpdateView, View
from AppOko.models import CategoryGallery, Chapters, Gallery, Products, SubCategories, CustomUser, ProductAbout, ProductDetails, ProductMedia, ProductTransaction, ProductTags, StaffUser, CustomerUser, GuestList, Categories, TempCustomerUser, AdminUser, ChatRoom, Message
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from oko.settings import BASE_URL
from django.views.decorators.csrf import csrf_exempt
import json as simplejson
import random
import string
import locale
import os, urllib
from oko import settings
try:
    from urllib import quote, unquote  # Python 2.X
except ImportError:
    from urllib.parse import quote, unquote
from django.contrib.auth.decorators import permission_required
from django.core.paginator import Paginator
from django.http import JsonResponse
import datetime

import locale
RU_MONTH_VALUES = {
    'January': 'января',
    'February': 'февраля',
    'March': 'марта',
    'April': 'апреля',
    'May': 'мая',
    'June': 'июня',
    'July': 'июля',
    'August': 'августа',
    'September': 'сентября',
    'October': 'октября',
    'November': 'ноября',
    'December': 'декабря',
}


def int_value_from_ru_month(date_str):
    for k, v in RU_MONTH_VALUES.items():
        date_str = date_str.replace(k, str(v))

    return date_str


@permission_required('AppOko.admin_permission2')
def admin_home(request):
    return render(request,"admin_templates/home.html")

def customer_home(request):
    return render(request,"main_templates/home.html")


class ChaptersListView(PermissionRequiredMixin, ListView):
    model=Chapters
    template_name="admin_templates/chapter_list.html"
    paginate_by=21
    permission_required = 'AppOko.admin_permission2'

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Chapters.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Chapters.objects.all().order_by(order_by)

        return cat
    

    def get_context_data(self,**kwargs):
        context=super(ChaptersListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Chapters._meta.get_fields()
        return context


class ChaptersCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model=Chapters
    success_message="Раздел добавлен"
    fields="__all__"
    template_name="admin_templates/chapter_create.html"
    permission_required = 'AppOko.admin_permission2'

class ChaptersUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model=Chapters
    success_message="Раздел обновлен!"
    fields="__all__"
    template_name="admin_templates/chapter_update.html"
    permission_required = 'AppOko.admin_permission2'


class ChapterDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        chapter_id=kwargs["id"]
        chapter=Chapters.objects.get(id=chapter_id)

        string = quote(settings.MEDIA_ROOT+"/"+str(chapter.thumbnail).replace("media","").replace("//","/"))
        string = urllib.parse.unquote(string,encoding=('utf-8'))
        string = unquote(string)
        chapter_dubl=Chapters.objects.filter(thumbnail=chapter.thumbnail)
        if not chapter.thumbnail == "nofoto.jpeg":
            if len(chapter_dubl) == 1:
                os.remove(string)
        chapter.delete()
        return redirect ("chapter_list")

class ChapterDublicate(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        chapter_id=kwargs["id"]
        chapter=Chapters.objects.get(id=chapter_id)
        chapter_dublicate=Chapters(title=chapter.title,url_slug=chapter.url_slug,thumbnail=chapter.thumbnail,description=chapter.description,is_active=chapter.is_active)
        chapter_dublicate.save()
        return redirect ("chapter_list")
        

class SubCategoriesListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=SubCategories
    template_name="admin_templates/sub_category_list.html"
    paginate_by=21

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=SubCategories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=SubCategories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(SubCategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

class SubCategoriesCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    model=SubCategories
    success_message="Подкатегория добавлена!"
    fields="__all__"
    template_name="admin_templates/sub_category_create.html"
    permission_required = 'AppOko.admin_permission2'

    def getdetails_for_sub_category_create(request):
        chapter_name = request.GET['chapter_ajax']
        result_set = []
        all_categories = []
        selected_chapter = Chapters.objects.get(title=chapter_name)
        all_categories = selected_chapter.categories_set.all()
        for category in all_categories:
            result_set.append({'cat_title': category.title,'cat_id' : category.id})
        
        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

    def get_context_data(self,**kwargs):
        context = super(SubCategoriesCreate,self).get_context_data(**kwargs)
        chapters = Chapters.objects.all()
        context['chapters'] = chapters
        return context
        

class SubCategoriesUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    model=SubCategories
    success_message="Подкатегория обновлена!"
    fields="__all__"
    template_name="admin_templates/sub_category_update.html"
    permission_required = 'AppOko.admin_permission2'


    def get_context_data(self,**kwargs):
        context = super(SubCategoriesUpdate,self).get_context_data(**kwargs)
        chapters = Chapters.objects.all()
        context['chapters'] = chapters
        categories = Categories.objects.all()
        context['categories'] = categories
        context['category_selected'] = self.get_object().category
        context['chapter_selected'] = self.get_object().chapter_id
        return context

class SubCategoryDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        subcategory_id=kwargs["id"]
        subcategory=SubCategories.objects.get(id=subcategory_id)


        string = quote(settings.MEDIA_ROOT+"/"+str(subcategory.thumbnail).replace("media","").replace("//","/"))
        string = urllib.parse.unquote(string,encoding=('utf-8'))
        string = unquote(string)
        subcategory_dubl=SubCategories.objects.filter(thumbnail=subcategory.thumbnail)
        if not subcategory.thumbnail == "nofoto.jpeg":
            if len(subcategory_dubl) == 1:
                os.remove(string)
        subcategory.delete()
        return redirect ("sub_category_list")

class SubCategoryDublicate(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        subcategory_id=kwargs["id"]
        subcategory=SubCategories.objects.get(id=subcategory_id)
        subcategory_dublicate=SubCategories(title=subcategory.title,url_slug=subcategory.url_slug,thumbnail=subcategory.thumbnail,description=subcategory.description,is_active=subcategory.is_active, chapter_id_id = subcategory.chapter_id_id)
        subcategory_dublicate.save()
        return redirect ("sub_category_list")

class CategoriesListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=Categories
    template_name="admin_templates/category_list.html"
    paginate_by=21

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=Categories.objects.filter(Q(title__contains=filter_val) | Q(description__contains=filter_val)).order_by(order_by)
        else:
            cat=Categories.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CategoriesListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=SubCategories._meta.get_fields()
        return context

class CategoriesCreate(PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'AppOko.admin_permission2'
    model=Categories
    success_message="Категория добавлена!"
    fields="__all__"
    template_name="admin_templates/category_create.html"

class CategoriesUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'AppOko.admin_permission2'
    model=Categories
    success_message="Категория обновлена!"
    fields="__all__"
    template_name="admin_templates/category_update.html"

class CategoryDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        category_id=kwargs["id"]
        category=Categories.objects.get(id=category_id)


        string = quote(settings.MEDIA_ROOT+"/"+str(category.thumbnail).replace("media","").replace("//","/"))
        string = urllib.parse.unquote(string,encoding=('utf-8'))
        string = unquote(string)
        category_dubl=Categories.objects.filter(thumbnail=category.thumbnail)
        if not category.thumbnail == "nofoto.jpeg":
            if len(category_dubl) == 1:
                os.remove(string)
        category.delete()
        return redirect ("category_list")

class CategoryDublicate(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        category_id=kwargs["id"]
        category=Categories.objects.get(id=category_id)
        category_dublicate=Categories(title=category.title,url_slug=category.url_slug,thumbnail=category.thumbnail,description=category.description,is_active=category.is_active, chapter_id_id = category.chapter_id_id)
        category_dublicate.save()
        return redirect ("category_list")

class ProductView(PermissionRequiredMixin, SuccessMessageMixin, View):
    permission_required = 'AppOko.admin_permission2'
    success_message="Продукт создан!"
    template_name="admin_templates/product_create.html"

    # def get_select(self, request):
    #     category_select2 = self.request.GET.get('category_select2',"")
    #     categories_select = Chapters.objects.filter(title__contains=category_select2)
    #     return 
    
    def getdetails(request):
        chapter_name = request.GET['chapter_ajax']
        result_set = []
        all_categories = []
        selected_chapter = Chapters.objects.get(title=chapter_name)
        all_categories = selected_chapter.categories_set.all()
        for category in all_categories:
            result_set.append({'cat_title': category.title,'cat_id' : category.id})
        
        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

    def getdetails2(request):
        result_set = []
        category_name = request.GET['category_ajax']
        all_subcategories = []
        selected_category = Categories.objects.get(title=category_name)
        all_subcategories = selected_category.subcategories_set.all()
        for subcategory in all_subcategories:
            result_set.append({'sub_title': subcategory.title,'sub_id' : subcategory.id})
        
        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')


    def get(self,request,*args,**kwargs):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            ProductView.getdetails(request)
        chapters_list=[]
        chapters=Chapters.objects.filter(is_active=1)
        for chapter in chapters:
            sub_category=SubCategories.objects.filter(is_active=1,chapter_id=chapter.id)
            category=Categories.objects.filter(is_active=1, chapter_id=chapter.id)
            category=Categories.objects.all()
            chapters_list.append({"chapter":chapter,"sub_category":sub_category, "category":category})

        staff_users = StaffUser.objects.filter(auth_user_id__is_active=True)

        return render(request, "admin_templates/product_create.html",{"chapters":chapters_list, "staff_users": staff_users})
        


    def post(self,request,*args,**kwargs):
        product_name=request.POST.get("product_name")
        size=request.POST.get("size")
        article=request.POST.get("article")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category_select")
        chapter=request.POST.get("chapter_select")
        category=request.POST.get("category_select")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        added_by_staff=request.POST.get("added_by_staff")
        in_stock_total=request.POST.get("in_stock_total",'1')
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")
        title_title_list=request.POST.getlist("title_title[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        product_tags=request.POST.get("product_tags")
        long_desc=request.POST.get("product_long_description")
        subcat_obj=SubCategories.objects.get(id=sub_category)
        cat_obj=Categories.objects.get(id=category)
        chap_obj = Chapters.objects.get(id=chapter)
        staff_user_obj=StaffUser.objects.get(id=added_by_staff)
        product=Products(product_name=product_name,in_stock_total=in_stock_total,url_slug=url_slug,size=size,article=article,subcategories_id=subcat_obj,chapters_id=chap_obj, categories_id=cat_obj, product_description=product_description,product_max_price=product_max_price,product_discount_price=product_discount_price,product_long_description=long_desc,added_by_staff=staff_user_obj)
        product.save()
        

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1
        if len(media_content_list) == 0:
            product_media=ProductMedia(product_id=product,media_type=media_type_list[0], media_content="/media/nofoto.jpeg")
            product_media.save()

        j=0
        for title_title in title_title_list:
            product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product_id=product)
            product_details.save()
            j=j+1

        for about_title in about_title_list:
            product_about=ProductAbout(title=about_title,product_id=product)
            product_about.save()
        
        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        
        product_transaction=ProductTransaction(product_id=product,transaction_type=1,transaction_product_count=in_stock_total,transaction_description="Intially Item Added in Stocks")
        product_transaction.save()
        messages.success(self.request,"Продукт создан")
        return HttpResponse("ок")
        


@csrf_exempt
def file_upload(request):
    file=request.FILES["file"]
    fs=FileSystemStorage()
    filename=fs.save(file.name,file)
    file_url=fs.url(filename)
    return HttpResponse('{"location": "'+BASE_URL+''+file_url+'"}')

class ProductListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=Products
    template_name="admin_templates/product_list.html"
    paginate_by=21

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            products=Products.objects.filter(Q(product_name__contains=filter_val) | Q(product_description__contains=filter_val)).order_by(order_by)
        else:
            products=Products.objects.all().order_by(order_by)

        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1, is_active=1).first()
            product_list.append({"product":product,"media":product_media})
        return product_list

    def get_context_data(self,**kwargs):
        context=super(ProductListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=Products._meta.get_fields()
        return context

        

class ProductEdit(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'

    def getdetails(request):
        category_name = request.GET['category_ajax']
        result_set = []
        all_subcategories = []
        selected_chapter = Chapters.objects.get(title=category_name)
        all_subcategories = selected_chapter.subcategories_set.all()
        for subcategory in all_subcategories:
            result_set.append({'title': subcategory.title,'id' : subcategory.id})
        return HttpResponse(simplejson.dumps(result_set), content_type='application/json')

    def get(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_details=ProductDetails.objects.filter(product_id=product_id)
        product_about=ProductAbout.objects.filter(product_id=product_id)
        product_tags=ProductTags.objects.filter(product_id=product_id)
        product_chapter = Chapters.objects.filter(id=product.chapters_id.id)
        if not product.categories_id == None:
            product_category = Categories.objects.filter(id = product.categories_id.id)
        else:
            product_category = Categories.objects.filter().first()
        product_subcategory = SubCategories.objects.filter(id=product.subcategories_id.id)

        chapters=Chapters.objects.filter(is_active=1)
        categories=Categories.objects.filter(is_active=1)
        sub_categories=SubCategories.objects.filter(is_active=1)
        return render(request,"admin_templates/product_edit.html", {"chapters":chapters,"categories":categories,"sub_categories":sub_categories,"product": product, "product_details":product_details, "product_about":product_about, "product_tags":product_tags, "product_chapter":product_chapter, "product_subcategory":product_subcategory, 'product_category':product_category })

    def post(self,request, *args, **kwargs):
        product_name=request.POST.get("product_name")
        size=request.POST.get("size")
        article=request.POST.get("article")
        url_slug=request.POST.get("url_slug")
        sub_category=request.POST.get("sub_category_select")
        chapter=request.POST.get("chapter_select")
        category=request.POST.get("category_select")
        product_max_price=request.POST.get("product_max_price")
        product_discount_price=request.POST.get("product_discount_price")
        product_description=request.POST.get("product_description")
        title_title_list=request.POST.getlist("title_title[]")
        details_ids=request.POST.getlist("details_id[]")
        title_details_list=request.POST.getlist("title_details[]")
        about_title_list=request.POST.getlist("about_title[]")
        about_ids=request.POST.getlist("about_id[]")
        product_tags=request.POST.get("product_tags")
        is_active="1"
        long_desc=request.POST.get("product_long_description")
        subcat_obj=SubCategories.objects.get(id=sub_category)
        chap_obj=Chapters.objects.get(id=chapter)
        cat_obj=Categories.objects.get(id=category)
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product.product_name=product_name
        product.url_slug=url_slug
        product.size=size
        product.article=article
        product.chapters_id=chap_obj
        product.categories_id=cat_obj
        product.subcategories_id=subcat_obj
        product.product_description=product_description
        product.product_max_price=product_max_price
        product.product_discount_price=product_discount_price
        product.product_long_description=long_desc
        product.is_active=is_active
        product.save()

        j=0
        for title_title in title_title_list:
            detail_id=details_ids[j]
            if detail_id == "blank" and title_title!="":
                product_details=ProductDetails(title=title_title,title_details=title_details_list[j],product_id=product)
                product_details.save()

            else:
                if title_title != "":
                    product_details=ProductDetails.objects.get(id=detail_id)
                    product_details.title=title_title
                    product_details.title_details=title_details_list[j]
                    product_details.product_id=product
                    product_details.save()
            j=j+1


        k=0
        for about in about_title_list:
            about_id=about_ids[k]
            if about_id == "blank" and about != "":
                product_about=ProductAbout(title=about,product_id=product)
                product_about.save()
            else:
                if about!="":
                    product_about=ProductAbout.objects.get(id=about_id)
                    product_about.title=about
                    product_about.product_id=product
                    product_about.save()
            k=k+1
        
        ProductTags.objects.filter(product_id=product_id).delete()

        product_tags_list=product_tags.split(",")

        for product_tag in product_tags_list:
            product_tag_obj=ProductTags(product_id=product,title=product_tag)
            product_tag_obj.save()
        
        return HttpResponse("ок")


class ProductAddMedia(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request, "admin_templates/product_add_media.html",{"product":product})

    def post(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        product = Products.objects.get(id=product_id)
        media_type_list=request.POST.getlist("media_type[]")
        media_content_list=request.FILES.getlist("media_content[]")

        i=0
        for media_content in media_content_list:
            fs=FileSystemStorage()
            filename=fs.save(media_content.name,media_content)
            media_url=fs.url(filename)
            product_media=ProductMedia(product_id=product,media_type=media_type_list[i],media_content=media_url)
            product_media.save()
            i=i+1

        return redirect ("product_list")

class ProductEditMedia(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        product_medias=ProductMedia.objects.filter(product_id=product_id)

        return render(request,"admin_templates/product_edit_media.html", {"product":product, "product_medias":product_medias})

class ProductDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        product_id=kwargs["id"]
        product=Products.objects.get(id=product_id)

        products_media = ProductMedia.objects.filter(product_id_id=product.id)
        for product_media in products_media:
            string = quote(settings.MEDIA_ROOT+str(product_media.media_content).replace("media","").replace("//","/"))
            string = urllib.parse.unquote(string,encoding=('utf-8'))
            string = unquote(string)
            if not product_media.media_content == "/media/nofoto.jpeg":
                productsmedia_with = ProductMedia.objects.filter(media_content=product_media.media_content)
                if len(productsmedia_with) == 1:
                    os.remove(string)
            product_media.delete()

        products_details = ProductDetails.objects.filter(product_id_id=product.id)
        for product_details in products_details:
            product_details.delete()

        products_about = ProductAbout.objects.filter(product_id_id=product.id)
        for product_about in products_about:
            product_about.delete()

        products_tags = ProductTags.objects.filter(product_id_id=product.id)
        for product_tags in products_tags:
            product_tags.delete()

        product.delete()
        return redirect ("product_list")
        
class ProductDublicate(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        product_id=kwargs["id"]
        product=Products.objects.get(id=product_id)
        product_dublicate=Products(url_slug=product.url_slug,product_name=product.product_name,product_max_price=product.product_max_price,product_discount_price=product.product_discount_price,product_description=product.product_description, product_long_description = product.product_long_description, in_stock_total = product.in_stock_total, is_active = product.is_active, added_by_staff_id = product.added_by_staff_id, chapters_id_id = product.chapters_id_id, subcategories_id_id = product.subcategories_id_id, article = product.article, size = product.size)
        product_dublicate.save()

        products_media = ProductMedia.objects.filter(product_id_id=product_id)
        for product_media in products_media:
            product_media_dublicate = ProductMedia(product_id_id=product_dublicate.id, media_type=product_media.media_type, media_content=product_media.media_content, is_active = product_media.is_active)
            product_media_dublicate.save()

        # product_transaction = ProductTransaction.objects.get(product_id_id = product_id)
        # product_transaction_dublicate = ProductTransaction(transaction_product_count = product_transaction.transaction_product_count, transaction_type = product_transaction.transaction_type, transaction_description = product_transaction.transaction_description)
        # product_transaction_dublicate.save()

        products_details = ProductDetails.objects.filter(product_id_id=product_id)
        for product_details in products_details:
            product_details_dublicate = ProductDetails(product_id_id = product_dublicate.id, title = product_details.title, title_details = product_details.title_details, is_active = product_details.is_active)
            product_details_dublicate.save()

        products_about = ProductAbout.objects.filter(product_id_id=product_id)
        for product_about in products_about:
            product_about_dublicate = ProductAbout(product_id_id = product_dublicate.id, title = product_about.title, is_active = product_about.is_active)
            product_about_dublicate.save()

        products_tags = ProductTags.objects.filter(product_id_id=product_id)
        for product_tags in products_tags:
            product_tags_dublicate = ProductTags(product_id_id = product_dublicate.id, title = product_tags.title, is_active = product_tags.is_active)
            product_tags_dublicate.save()

        return redirect ("product_list")

class ProductMediaDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        media_id=kwargs["id"]
        product_media=ProductMedia.objects.get(id=media_id)

        string = quote(settings.MEDIA_ROOT+str(product_media.media_content).replace("media","").replace("//","/"))
        string = urllib.parse.unquote(string,encoding=('utf-8'))
        string = unquote(string)
        if not product_media.media_content == "/media/nofoto.jpeg":
            productsmedia_with = ProductMedia.objects.filter(media_content=product_media.media_content)
            if len(productsmedia_with) == 1:
                os.remove(string)
        
        product_id=product_media.product_id.id
        product_media.delete()
        return HttpResponseRedirect(reverse("product_edit_media",kwargs={"product_id":product_id}))

class ProductAddStocks(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        product=Products.objects.get(id=product_id)
        return render(request,"admin_templates/product_add_stocks.html", {"product":product})

    def post(self, request, *args, **kwargs):
        product_id=kwargs["product_id"]
        new_instock=request.POST.get("add_stocks")
        product=Products.objects.get(id=product_id)
        old_stocks=product.in_stock_total
        new_stock=int(new_instock)+int(old_stocks)
        product.in_stock_total = new_stock
        product.save()

        product_obj=Products.objects.get(id=product_id)
        product_transaction=ProductTransaction(product_id=product_obj, transaction_product_count=new_instock, transaction_description="New Product Added", transaction_type=1)
        product_transaction.save()
        return HttpResponseRedirect(reverse("product_add_stocks", kwargs={"product_id":product_id}))


class StaffUserListView(PermissionRequiredMixin,ListView):
    permission_required = 'AppOko.admin_permission2'
    model=StaffUser
    template_name="admin_templates/staff_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=StaffUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=StaffUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(StaffUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=StaffUser._meta.get_fields()
        return context


class StaffUserCreateView(PermissionRequiredMixin, SuccessMessageMixin,CreateView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/staff_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for staff User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=2
        user.set_password(form.cleaned_data["password"])
        user.save()

        # #Saving staff user
        
        staffuser=StaffUser.objects.get(auth_user_id=user.id)

        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        staffuser.profile_pic=profile_pic_url
        staffuser.save()

        messages.success(self.request,"Staff User Created")
        return HttpResponseRedirect(reverse("staff_list"))

class StaffUserUpdateView(PermissionRequiredMixin, SuccessMessageMixin,UpdateView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/staff_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        staffuser=StaffUser.objects.get(auth_user_id=self.object.pk)
        context["staffuser"]=staffuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Staff User
        user=form.save(commit=False)
        user.save()

        #Saving Staff user
        staffuser=StaffUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            staffuser.profile_pic=profile_pic_url

        staffuser.save()
        messages.success(self.request,"Staff User Updated")
        return HttpResponseRedirect(reverse("staff_list"))


class CustomerUserListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=CustomerUser
    template_name="admin_templates/customer_list.html"
    paginate_by=3

    def get(self, request):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=CustomerUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=CustomerUser.objects.all().order_by(order_by)
        my_host=request.get_host()
        return render(request,"admin_templates/customer_list.html", {"my_host":my_host, 'customeruser_list':cat})

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=CustomerUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=CustomerUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(CustomerUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=CustomerUser._meta.get_fields()
        return context

class CustomerUserCreateView(PermissionRequiredMixin, SuccessMessageMixin,CreateView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/customer_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for staff User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        
        customeruser=CustomerUser.objects.get(auth_user_id=user.id)

        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)
        customeruser.profile_pic=profile_pic_url
        customeruser.save()

        messages.success(self.request,"Customer User Created")
        return HttpResponseRedirect(reverse("customer_list"))

class CustomerUserRandomCreateView(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request):
        id_new_user = CustomUser.objects.latest('id').id+1
        username = "User"+str(id_new_user)

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        length = 16
        all = lower + upper + num + symbols
        temp = random.sample(all,length)
        password = "".join(temp)

        user=CustomUser(first_name="", last_name="", email="", username=username, password = password)
        user.is_active=True
        user.user_type=3

            # all = string.ascii_letters + string.digits + string.punctuation
            # pass = "".join(random.sample(all,length))
        user.save()

            
        customeruser=CustomerUser.objects.get(auth_user_id=user.id)

        profile_pic=''
        customeruser.profile_pic=profile_pic
        customeruser.save()
        return redirect ("customer_list")

class CustomerUserUpdateView(PermissionRequiredMixin, SuccessMessageMixin,UpdateView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/customer_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        customeruser=CustomerUser.objects.get(auth_user_id=self.object.pk)
        context["CustomerUser"]=customeruser
        return context

    def form_valid(self,form):

        user=form.save(commit=False)
        user.save()


        customeruser=CustomerUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            customeruser.profile_pic=profile_pic_url

        customeruser.save()
        messages.success(self.request,"Customer User Updated")
        return HttpResponseRedirect(reverse("customer_list"))

class TempCustomerUserListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=TempCustomerUser
    template_name="admin_templates/tempcustomer_list.html"
    paginate_by=10

    def get(self, request):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=TempCustomerUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=TempCustomerUser.objects.all().order_by(order_by)
        my_host=request.get_host()
        return render(request,"admin_templates/tempcustomer_list.html", {"my_host":my_host, 'tempcustomeruser_list':cat})

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=TempCustomerUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=TempCustomerUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(TempCustomerUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=TempCustomerUser._meta.get_fields()
        return context

class TempCustomerUserCreateView(PermissionRequiredMixin, SuccessMessageMixin,CreateView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/tempcustomer_create.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for staff User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=4
        user.set_password(form.cleaned_data["password"])
        user.save()

        
        tempcustomeruser=TempCustomerUser.objects.create(auth_user_id=CustomUser.objects.get(id=user.id))
        profile_pic=self.request.FILES.get("profile_pic2")
        if profile_pic != None:
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            tempcustomeruser.profile_pic=profile_pic_url
            tempcustomeruser.save()

        messages.success(self.request,"TempCustomer User Created")
        return HttpResponseRedirect(reverse("tempcustomer_list"))

class TempCustomerUserRandomCreateView(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,**kwargs):
        
        id_new_user = CustomUser.objects.latest('id').id+1
        username = "User"+str(id_new_user)

        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        num = string.digits
        symbols = string.punctuation
        length = 16
        all = lower + upper + num + symbols
        temp = random.sample(all,length)
        password = "".join(temp)

        user=CustomUser(first_name="", last_name="", email="", username=username, password = password)
        user.is_active=True
        user.user_type=4

            # all = string.ascii_letters + string.digits + string.punctuation
            # pass = "".join(random.sample(all,length))
        user.save()
        project=kwargs["id"]
        tempcustomeruser=TempCustomerUser.objects.create(profile_pic='',auth_user_id=CustomUser.objects.get(id=user.id),project_id=project)

        profile_pic=''
        tempcustomeruser.profile_pic=profile_pic
        tempcustomeruser.save()
        return redirect ("tempcustomer_list")

class TempCustomerUserUpdateView(PermissionRequiredMixin, SuccessMessageMixin,UpdateView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/tempcustomer_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        tempcustomeruser=TempCustomerUser.objects.get(auth_user_id=self.object.pk)
        context["TempCustomerUser"]=tempcustomeruser
        return context

    def form_valid(self,form):

        user=form.save(commit=False)
        user.save()


        tempcustomeruser=TempCustomerUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            tempcustomeruser.profile_pic=profile_pic_url

        tempcustomeruser.save()
        messages.success(self.request,"TempCustomer User Updated")
        return HttpResponseRedirect(reverse("tempcustomer_list"))


class GuestListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/guest_list.html"
    fields=["id","ip","time","count_ip","last_time"]
    model=GuestList


    def get(self,request):
        unique_ips = GuestList.objects.all().values_list('ip', flat=True).distinct()
        last_times = GuestList.objects.all().values_list("last_time")
        guestlists = GuestList.objects.filter(ip__in=unique_ips, time__in=last_times).order_by("-last_time")
        guestlists_list=[]
        for guestlist in guestlists:
            guestlists_list.append({"guestlist":guestlist})
        viewlists=GuestList.objects.all().order_by("-time")
        viewlists_list=[]
        for viewlist in viewlists:
            viewlists_list.append({"viewlist":viewlist})
        view_paginator = Paginator(viewlists_list, per_page=10)
        view_page = request.GET.get('page')
        view_page_object = view_paginator.get_page(view_page)
        guest_paginator = Paginator(guestlists_list, per_page=10)
        guest_page = request.GET.get('page')
        guest_page_object = guest_paginator.get_page(guest_page)
        return render(request, "admin_templates/guest_list.html",{"guestlists":guestlists_list,"viewlists":viewlists_list, "view_page_obj": view_page_object, "guest_page_obj": guest_page_object})

class GalleryCreate(PermissionRequiredMixin, SuccessMessageMixin, View):
    permission_required = 'AppOko.admin_permission2'
    success_message="Фото добавлено!"
    template_name="admin_templates/gallery_create.html"


    def post(self,request, *args, **kwargs):
        media_content_list = []
        media_content_list=request.FILES.getlist("media_content[]")
        title=request.POST.get("title")
        type_of_product=request.POST.get("type_of_product")
        type_of_product=CategoryGallery(id=type_of_product)
        description=request.POST.get("description")
        customer=request.POST.get("customer")
        order_number=request.POST.get("order_number")
        i=0


        
        for media_content in media_content_list:
            fs=FileSystemStorage(location="media/gallery/")
            filename=fs.save(media_content.name,media_content)
            filename_for_gallery="gallery/"+filename
            media_url=fs.url(filename_for_gallery)
            photo=Gallery(title=title, type_of_product=type_of_product, description=description, customer=customer, order_number=order_number, media_content=media_url, is_active=1)
            photo.save()
            i=i+1
        
        messages.success(self.request,"Фото добавлены")
        return HttpResponse("ок")
    
    def get(self, request):
        categories_for_gallery = CategoryGallery.objects.all()
        return render(request,"admin_templates/gallery_create.html", {'categories_for_gallery':categories_for_gallery})



class GalleryUpdate(PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'AppOko.admin_permission2'
    model=Gallery
    success_message="Категория обновлена!"
    fields="__all__"
    template_name="admin_templates/category_update.html"

    def post(self,request, *args, **kwargs):
        title=request.POST.get("title")
        type_of_product=request.POST.get("type_of_product")
        type_of_product=CategoryGallery(id=type_of_product)
        description=request.POST.get("description")
        customer=request.POST.get("customer")
        order_number=request.POST.get("order_number")
        is_active=request.POST.get("is_active")
        

        gallery_id=kwargs["id"]
        gallery = Gallery.objects.get(id=gallery_id)
        gallery.title = title
        gallery.type_of_product = type_of_product
        gallery.description = description
        gallery.customer = customer
        gallery.order_number = order_number
        gallery.is_active = is_active
        gallery.save()
        messages.success(self.request,"Фото обновлено")
        return HttpResponse("ок")
    
    def get(self, request,**kwargs):
        gallery_id=kwargs["id"]
        gallery = Gallery.objects.get(id=gallery_id)
        categories_for_gallery = CategoryGallery.objects.all()
        return render(request,"admin_templates/gallery_update.html", {"photo":gallery, "categories_for_gallery":categories_for_gallery})

class GalleryDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        gallery_id=kwargs["id"]
        gallery=Gallery.objects.get(id=gallery_id)


        string = quote(settings.MEDIA_ROOT+"/"+str(gallery.media_content).replace("media","").replace("//","/"))
        string = urllib.parse.unquote(string,encoding=('utf-8'))
        string = unquote(string)
        gallery_dubl=Gallery.objects.filter(media_content=gallery.media_content)
        if not gallery.media_content == "nofoto.jpeg":
            if len(gallery_dubl) == 1:
                os.remove(string)
        gallery.delete()
        return redirect ("gallery_list")

class GalleryDublicate(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    def get(self,request,*args,**kwargs):
        gallery_id=kwargs["id"]
        gallery=Gallery.objects.get(id=gallery_id)
        gallery_dublicate=Gallery(title=gallery.title,type_of_product=gallery.type_of_product,media_content=gallery.media_content,description=gallery.description,is_active=gallery.is_active, customer = gallery.customer, order_number = gallery.order_number)
        gallery_dublicate.save()
        return redirect ("gallery_list")


class GalleryListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=Gallery
    template_name="admin_templates/gallery_list.html"
    paginate_by=21

    def get_queryset(self):
        filter_val_photo=self.request.GET.get("filter_photo")
        order_by_photo=self.request.GET.get("orderby_photo","id")
        filter_val_category_photo=self.request.GET.get("filter_category_photo")
        if filter_val_category_photo =="":
            photos=Gallery.objects.all().order_by(order_by_photo)
        elif filter_val_category_photo != None:
            filter_val_category_photo=CategoryGallery.objects.filter(title=filter_val_category_photo)
            photos=Gallery.objects.filter(type_of_product=filter_val_category_photo[0].id).order_by(order_by_photo)
        else:
            if filter_val_photo!=None:
                photos=Gallery.objects.filter(Q(title__iregex=filter_val_photo) | Q(customer__iregex=filter_val_photo ) | Q(description__iregex=filter_val_photo)).order_by(order_by_photo)
            else:
                photos=Gallery.objects.all().order_by(order_by_photo)



        photo_list=[]
        for photo in photos:
            photo_list.append({"photo":photo})
        return photo_list

    def get_context_data(self,**kwargs):
        context=super(GalleryListView,self).get_context_data(**kwargs)
        context["filter_photo"]=self.request.GET.get("filter_photo","")
        context["orderby_photo"]=self.request.GET.get("orderby_photo","id")
        context["all_table_fields"]=Gallery._meta.get_fields()
        context["categories"]=CategoryGallery.objects.all()
        context["filter_val_category_photo"]=self.request.GET.get("filter_val_category_photo","")
        return context

class CategoryGalleryCreate(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'
    success_message="Категория создана!"
    template_name="admin_templates/category_for_gallery_create.html"

    def getdetails_for_category_gallery_create(request):
        type_of_product_for_delete_ajax = request.GET['type_of_product_for_delete_ajax']
        selected_category_for_gallery = CategoryGallery.objects.get(title=type_of_product_for_delete_ajax)
        result = selected_category_for_gallery.id
        return HttpResponse(simplejson.dumps(result), content_type='application/json')

    def post(self,request, *args, **kwargs):
        title2=request.POST.get("title2")
        is_active="1"
        category_for_gallery=CategoryGallery(title=title2,is_active=is_active)
        category_for_gallery.save()
        messages.success(self.request,"Категория добавлена")
        return HttpResponse("ок")
    
    def get_context_data(self, request):
        title=request.POST.get("title")
        type_of_product=request.POST.get("type_of_product")
        description=request.POST.get("description")
        customer=request.POST.get("customer")
        order_number=request.POST.get("order_number")
        is_active=request.POST.get("is_active")
        return render(request,"admin_templates/gallery_create.html", {'title2':title, 'type_of_product2':type_of_product, 'description2':description, 'customer2':customer, 'order_number2':order_number, 'is_active2':is_active})


class CategoryGalleryDelete(PermissionRequiredMixin, View):
    permission_required = 'AppOko.admin_permission2'

    def get(self,request,*args,**kwargs):
        category_id=kwargs["id"]
        category_for_gallery_id=CategoryGallery.objects.filter(id=category_id)
        category_for_gallery_id.delete()
        return redirect ("gallery_create")
        


from http.client import HTTPResponse
from django.shortcuts import render
import pandas as pd
import os
from django.core.files.storage import FileSystemStorage
from .models import Projects
 
# Create your views here.
@permission_required('AppOko.admin_permission2')
def Import_Excel_pandas(request):
    filename = "media/spisok.xls"
    empexceldata = pd.read_excel(filename)    
    dbframe = empexceldata
    names_project = []
    for dbframe in dbframe.itertuples():
        dublicate_project = Projects.objects.filter(number = dbframe.Номер)
        if not dublicate_project:
            obj = Projects.objects.create(date=dbframe.Дата,number=dbframe.Номер, name=dbframe.Наименование,
                                            client=dbframe.Контрагент, manager=dbframe.Менеджер)
            obj.save()
        if dublicate_project:
            obj = Projects.objects.filter(number=dbframe.Номер).first()
            obj.date =  dbframe.Дата
            obj.name = dbframe.Наименование
            obj.client = dbframe.Контрагент
            obj.manager = dbframe.Менеджер
            obj.save()
        names_project.append(str(dbframe.Номер))
    objects = Projects.objects.all()
    for obj in objects:
        x = str(obj.number)
        if x not in names_project:
            obj.delete()
    return render(request, 'admin_templates/projects_list.html') 

class ProjectListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    template_name="admin_templates/projects_list.html"
    fields=["date","number","name","client","manager"]
    model=Projects

    def get(self,request):
        Import_Excel_pandas(request)
        projects = Projects.objects.all()
        project_paginator = Paginator(projects, per_page=30)
        project_page = request.GET.get('page')
        project_page_object = project_paginator.get_page(project_page)
        return render(request, "admin_templates/projects_list.html", {'projects':projects,'project_page_obj': project_page_object})
 
class ChatListView(PermissionRequiredMixin, ListView):
    permission_required = 'AppOko.admin_permission2'
    model=ChatRoom
    template_name="admin_templates/chat_list.html"
    def get_queryset(self):

        filter_val=self.request.GET.get("filter","")
        if filter_val!="":
            room = ChatRoom.objects.get(host_id=filter_val)
            messages=Message.objects.filter(room_id=room).order_by("created")
            user_for_chat = CustomUser.objects.get(id=filter_val)
        else:
            messages=''
            #передается object_list
        return messages

    def post(self, request):
        if self.request.method == "POST":
            if self.request.POST.get("form_type") == 'message_type':
                room = self.request.GET.get("filter")
                room = ChatRoom.objects.get(host=room)
                Message.objects.create(
                    user = self.request.user,
                    room = room,
                    body = self.request.POST.get("body")
                )
                room=str(room.host_id)
                redirect_url = reverse('chat_list')
                return redirect(f'{redirect_url}?filter={room}')

    def get_context_data(self, *args,**kwargs):
        filter_val=self.request.GET.get("filter","")
        if filter_val!="":
            user = CustomerUser.objects.filter(auth_user_id=filter_val).values_list('auth_user_id')
        else:
            user = ''
        rooms = ChatRoom.objects.filter(host_id__in=user)
        messages=Message.objects.filter(room__in=rooms).order_by("created")
        room_list=[]
        for i in rooms:
            room = i.host_id
            username = CustomUser.objects.get(id=i.host_id).username
            room_list.append({"room":room, "username":username})

        client_user=CustomerUser.objects.all().values_list('auth_user_id')
        rooms_for_client_list = ChatRoom.objects.filter(host_id__in=client_user)
        rooms_for_client_list_list=[]
        for i in rooms_for_client_list:
            room = i.host.id
            username = CustomUser.objects.get(id=i.host_id).username
            rooms_for_client_list_list.append({"room":room, "username":username})
        if filter_val != '':
            room_of_filter=ChatRoom.objects.get(host_id=filter_val).id
        else:
            room_of_filter=''
        context=super().get_context_data(*args,**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["messages"]=messages
        context["room_of_filter"]=room_of_filter
        context["rooms"]=room_list
        context["rooms_for_client_list"]=rooms_for_client_list_list
        return context


def chatmessage_send(request):
    body = request.GET['body']
    if body == "":
        result = ""
        return HttpResponse(simplejson.dumps(result), content_type='application/json')
    room_id = request.GET['room_id']
    user_id = request.GET['user_id']
    host_id = request.GET['host_id']
    if room_id == '':
        room_id2 = ChatRoom.objects.get(host_id=host_id)
    else:
        room_id2 = ChatRoom.objects.get(id=room_id)
    user_id2 = CustomUser.objects.get(id=user_id)
    new_message = Message.objects.create(user=user_id2, room=room_id2, body=body)
    user_type = user_id2.user_type
    username = user_id2.username
    result = []

    message_text_created = new_message.created
    message_text_updated = new_message.updated

    message_text_created = str(new_message).split('.')[0]
    message_text_created = str(new_message.created.strftime('%d %B %Y г. %H:%M'))
    message_text_created = int_value_from_ru_month(message_text_created)
    message_text_updated = str(message_text_updated.strftime('%d %B %Y, %H:%M'))


    result.append({
            "user_id": username,
            "body": body,
            "room_id": room_id,
            "created": message_text_created,
            "updated": message_text_updated,
            "user_type": user_type
        })
    return HttpResponse(simplejson.dumps(result), content_type='application/json')

def chatmessage_check(request):
    room_id = request.GET['room_id']
    host_id = request.GET['host_id']
    if room_id == '':
        room_id2 = ChatRoom.objects.get(host_id=host_id)
    else:
        room_id2 = ChatRoom.objects.get(id=room_id)
    user_id = request.GET['user_id']
    user_id2 = CustomUser.objects.get(id=user_id)
    # if user_id == None:
    #     user_id == room_id2.host_id
    # all_messages_list = request.GET['all_messages_list']
    # print(all_messages_list)
    last_date = datetime.datetime.now()
    first_date= datetime.datetime.now() - datetime.timedelta(seconds=3.1)
    all_messages = Message.objects.filter(room=room_id2,created__range=(first_date, last_date)).exclude(user_id=user_id)
    print(all_messages)
    # print(all_messages)
    result = []
    for message in all_messages:
        user_id3 = CustomUser.objects.get(id=message.user_id)
        user_type = user_id3.user_type
        username = user_id3.username
        print(username)
        result = []
        body = message.body
        message_text_created = message.created
        message_text_updated = message.updated
        
        message_text_created = str(message).split('.')[0]
        message_text_created = str(message.created.strftime('%d %B %Y г. %H:%M'))
        message_text_created = int_value_from_ru_month(message_text_created)
        message_text_updated = str(message_text_updated.strftime('%d %B %Y, %H:%M'))

        result.append({
                "username": username,
                "body": body,
                "room_id": room_id,
                "created": message_text_created,
                "updated": message_text_updated,
                "user_type": user_type
            }) 
        print(result)
    user_type = user_id2.user_type
    username = user_id2.username

    if all_messages.exists():
        # result.append({
        #         "messages": messages,
        #     })
        return HttpResponse(simplejson.dumps(result), content_type='application/json')
    result2 = ""
    return HttpResponse(simplejson.dumps(result2), content_type='application/json')