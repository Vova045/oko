from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from django.urls import reverse
import urllib
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from AppOko.models import Gallery, GuestList, Chapters, Categories, Products, ProductMedia, SubCategories, CategoryGallery
from oko.settings import MEDIA_ROOT, MEDIA_URL
from django.db.models import Q
from django.core.mail import send_mail

# from django.http import HttpResponse
# import json as simplejson
# def getdetails(request):
#     category_name = request.GET['category_select']
#     print (category_name)
#     result_set = []
#     all_subcategories = []
#     answer = str(category_name[1:-1])
#     selected_category = Chapters.objects.get(title=answer)
#     all_subcategories = selected_category.subcategories_set.all()
#     for subcategory in all_subcategories:
#         result_set.append({'title': subcategory.title})
#     return HttpResponse(simplejson.dumps(result_set), mimetype='application/json', content_type='application/json')
        

def send_gmail(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            message_name = request.POST.get('message_name')
            message = request.POST.get('message')
            telephone = request.POST.get('telephone')
            msg=(f"Поступила заявка от {message_name}, его телефонный номер {telephone}. Вот его сообщение: {message}")
            return render (request, 'main_templates/home.html', {'msg': msg, 'recaptcha_site_key':settings.RECAPTCHA_PUBLIC_KEY})
        elif request.POST.get("form_type") == 'formTwo':
            msg = request.POST.get('g-recaptcha_msg')
            subject='Новая заявка'
            form_email = settings.EMAIL_HOST_USER
            if request.recaptcha_is_valid:
                send_mail(subject, msg, form_email,
    ['vovatsar@bk.ru','reklama-oko@mail.ru'], fail_silently=False)
                return render (request, 'main_templates/home.html', {'message_name': msg, 'recaptcha_site_key':settings.RECAPTCHA_PUBLIC_KEY})
        return render (request, 'main_templates/home.html',)
    else:
        return render (request, 'main_templates/home.html',) 

def get_id(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')

    
    GuestList.objects.create(ip=ip)

    if not GuestList.objects.filter(ip=ip).exists():
        last_time = GuestList.objects.filter(ip=ip).values_list('time').latest('time')[0]
        GuestList.objects.filter(ip=ip).update(last_time=last_time, count_ip = 1)

    else:
        count_ip = GuestList.objects.filter(ip=ip).count()
        last_time = GuestList.objects.filter(ip=ip).values_list('time').latest('time')[0]
        GuestList.objects.filter(ip=ip).update(count_ip=count_ip, last_time=last_time)
    
    return HttpResponseRedirect(reverse("guest_list"))


def home(request):
    
    get_id(request)
    if request.method == "POST":
        return send_gmail(request)

    photos = Gallery.objects.all()
    first_photo = Gallery.objects.all().first
    categories = CategoryGallery.objects.all()
    user = request.GET.get('user')
    print(user)
    password = request.GET.get('password')
    return render (request, 'main_templates/home.html', {'photos':photos, 'first_photo':first_photo, 'categories':categories, 'user':user, 'password':password})


from django.views.generic import ListView
from AppOko.models import Products

class SubcategoryListView(ListView):
    model=Products
    template_name="main_templates/detsad.html"
    products_subcategories_id = Products.objects.all().values_list("subcategories_id")
    subcategories = SubCategories.objects.filter(
        id__in=products_subcategories_id
    )
    queryset = Products.objects.filter(subcategories_id__in=subcategories.values_list("id"))
    paginate_by = 12
    context_object_name = "products"

    def get_queryset(self, **kwargs):
        get_value = self.kwargs['url_slug']
        get_value = urllib.parse.unquote(get_value,encoding=('cp1251'))
        subcategory_select = SubCategories.objects.filter(url_slug=get_value)
        products = Products.objects.filter(subcategories_id=subcategory_select.first())
        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1, is_active=1).first()
            product_list.append({"product":product,"media":product_media})
        return product_list
    
    def get_context_data(self,**kwargs):
        context = super(SubcategoryListView,self).get_context_data(**kwargs)

        products_chapters_id=Products.objects.all().values_list("chapters_id")
        chapters = Chapters.objects.filter(
        id__in=products_chapters_id
        )
        products_subcategories_id = Products.objects.all().values_list("subcategories_id")
        subcategories = SubCategories.objects.filter(id__in=products_subcategories_id)
        
    
        get_value = self.kwargs['url_slug']
        get_value = urllib.parse.unquote(get_value,encoding=('cp1251'))
        subcategory_select = SubCategories.objects.filter(url_slug=get_value)
        subcategory_kwards = get_value
        print1 = subcategory_select[0].chapter_id
        chapters_with_sub = Chapters.objects.filter(title=print1)
        chapters = Chapters.objects.all()
        subcategories = SubCategories.objects.all()
        categories = Categories.objects.all()


        get_value = self.kwargs['url_slug']
        get_value = urllib.parse.unquote(get_value,encoding=('cp1251'))
        subcategory_select = SubCategories.objects.filter(url_slug=get_value)
        count_product = Products.objects.filter(subcategories_id=subcategory_select.first()).count()
        paginate_by = SubcategoryListView.paginate_by

        context['chapters'] = chapters
        context['subcategories'] = subcategories
        context['subcategory_kwards'] = subcategory_kwards
        context['chapters_with_sub'] = chapters_with_sub[0]
        context['count_product'] = count_product
        context['paginate_by'] = paginate_by
        context['categories'] = categories

        return context


class CategoryListView(ListView):
    model=Products
    template_name="main_templates/detsad.html"
    products_subcategories_id = Products.objects.all().values_list("categories_id")
    subcategories = SubCategories.objects.filter(
        id__in=products_subcategories_id
    )
    queryset = Products.objects.filter(subcategories_id__in=subcategories.values_list("id"))
    ordering=["id"]
    paginate_by = 12
    context_object_name = "products"

    def get_queryset(self, **kwargs):
        get_value = self.kwargs['url_slug']
        get_value = urllib.parse.unquote(get_value,encoding=('cp1251'))
        subcategory_select = SubCategories.objects.filter(url_slug=get_value)
        products = Products.objects.filter(subcategories_id=subcategory_select.first())
        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1, is_active=1).first()
            product_list.append({"product":product,"media":product_media})
        return product_list
    
    def get_context_data(self,**kwargs):
        context = super(SubcategoryListView,self).get_context_data(**kwargs)

        products_chapters_id=Products.objects.all().values_list("chapters_id")
        chapters = Chapters.objects.filter(
        id__in=products_chapters_id
        )
        products_subcategories_id = Products.objects.all().values_list("subcategories_id")
        subcategories = SubCategories.objects.filter(id__in=products_subcategories_id)
        
    
        get_value = self.kwargs['url_slug']
        get_value = urllib.parse.unquote(get_value,encoding=('cp1251'))
        subcategory_select = SubCategories.objects.filter(url_slug=get_value)
        subcategory_kwards = get_value
        print1 = subcategory_select[0].chapter_id
        chapters_with_sub = Chapters.objects.filter(title=print1)
        chapters = Chapters.objects.all()
        subcategories = SubCategories.objects.all()
        categories = Categories.objects.all()


        get_value = self.kwargs['url_slug']
        get_value = urllib.parse.unquote(get_value,encoding=('cp1251'))
        subcategory_select = SubCategories.objects.filter(url_slug=get_value)
        count_product = Products.objects.filter(subcategories_id=subcategory_select.first()).count()
        paginate_by = SubcategoryListView.paginate_by

        context['chapters'] = chapters
        context['subcategories'] = subcategories
        context['subcategory_kwards'] = subcategory_kwards
        context['chapters_with_sub'] = chapters_with_sub[0]
        context['count_product'] = count_product
        context['paginate_by'] = paginate_by
        context['categories'] = categories

        return context



class ChapterListView(ListView):
    model=Products
    template_name="main_templates/detsad.html"
    products_chapters_id=Products.objects.all().values_list("chapters_id")
    chapters = Chapters.objects.filter(
        id__in=products_chapters_id
        )

    queryset = Products.objects.filter(chapters_id__in=chapters.values_list("id"))
    ordering=['id']
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self, **kwargs):
        products = Products.objects.filter(chapters_id=self.kwargs['pk'])
        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1, is_active=1).first()
            product_list.append({"product":product,"media":product_media})
        return product_list
    
    def get_context_data(self,**kwargs):
        context = super(ChapterListView,self).get_context_data(**kwargs)
        products_chapters_id=Products.objects.all().values_list("chapters_id")
        chapters = Chapters.objects.filter(
        id__in=products_chapters_id
        )
        products_subcategories_id = Products.objects.all().values_list("subcategories_id")
        subcategories = SubCategories.objects.filter(id__in=products_subcategories_id)
        chapter_kwards = self.kwargs['pk']
        chapters = Chapters.objects.all()
        subcategories = SubCategories.objects.all()
        categories = Categories.objects.all()
        context['chapters'] = chapters
        context['subcategories'] = subcategories
        context['chapter_kwards'] = chapter_kwards
        context['categories'] = categories
        return context
    
    
class DetsadListView(ListView):
    model=Products
    template_name="main_templates/detsad.html"
    products_chapters_id=Products.objects.all().values_list("chapters_id")
    chapters = Chapters.objects.filter(
        id__in=products_chapters_id
        )
    queryset = Products.objects.filter(chapters_id__in=chapters.values_list("id"))
    ordering=['id']
    paginate_by = 12
    context_object_name = 'products'
    

    def get_queryset(self, **kwargs):
        products=super().get_queryset(**kwargs)
        product_list=[]
        for product in products:
            product_media=ProductMedia.objects.filter(product_id=product.id,media_type=1, is_active=1).first()
            product_list.append({"product":product,"media":product_media})
            
        return product_list

    def get_context_data(self,**kwargs):
        context = super(DetsadListView,self).get_context_data(**kwargs)
        products_chapters_id=Products.objects.all().values_list("chapters_id")
        chapters = Chapters.objects.filter(
        id__in=products_chapters_id
        )
        products_subcategories_id = Products.objects.all().values_list("subcategories_id")
        subcategories = SubCategories.objects.filter(id__in=products_subcategories_id)
        chapters = Chapters.objects.all()
        subcategories = SubCategories.objects.all()
        categories = Categories.objects.all()
        context['chapters'] = chapters
        context['subcategories'] = subcategories
        context['categories'] = categories
        return context


class GalleryListView(ListView):
    model=Gallery
    template_name="main_templates/home.html"
    queryset = Gallery.objects.all()
    ordering=["id"]
    paginate_by = 12
    context_object_name = "photos"

    def get_queryset(self, **kwargs):
        photos=super().get_queryset(**kwargs)
        photo_list=[]
        for photo in photos:
            photo_list.append({"photo":photo})
            
        return photo_list
    
    def get_context_data(self,**kwargs):
        context = super(GalleryListView,self).get_context_data(**kwargs)
        photos = Gallery.objects.all()
        context['photos'] = photos

        return context


#ADMIN FUNCTION
def adminLogin(request):
    return render(request,"admin_templates/signin.html")

def adminLoginProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")

    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request,"Error in Login! Invalid Login Details")
        return HttpResponseRedirect(reverse("admin_login"))
    
def adminLogoutProcess(request):
    logout(request)
    messages.success(request,"Logout Succesfully")
    return HttpResponseRedirect(reverse("admin_login"))

def bukvy(request):
    return render (request, 'main_templates/bukvy.html',) 