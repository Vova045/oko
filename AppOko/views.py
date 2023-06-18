from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.urls import reverse
import urllib
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from AppOko.models import Gallery, GuestList, Chapters, Categories, Products, ProductMedia, SubCategories, CategoryGallery, TempCustomerUser, CustomerUser,Projects, ChatRoom, Message, AdminUser, AdminChatRooms, AdminChatMessage, AdminChatMessageMedia, AdminChatReadMessage
from oko.settings import MEDIA_ROOT, MEDIA_URL
from django.db.models import Q
from django.core.mail import send_mail
from django.contrib.auth.models import Permission

def send_gmail(request):
    if request.method == 'POST':
        if request.POST.get("form_type") == 'mail_type':
            message_name = request.POST.get('message_name')
            message = request.POST.get('message')
            telephone = request.POST.get('telephone')
            msg=(f"Поступила заявка от {message_name}, его телефонный номер {telephone}. Вот его сообщение: {message}")
            return render (request, 'main_templates/home.html', {'msg': msg, 'recaptcha_site_key':settings.RECAPTCHA_PUBLIC_KEY})
        elif request.POST.get("form_type") == 'captcha_type':
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
        if request.POST.get("form_type") == 'mail_type' or request.POST.get("form_type") == 'captcha_type':
            return send_gmail(request)

    # Добавление разрешения для пользователей
    user_for_permission = CustomUser.objects.filter(user_type="1")
    ct = ContentType.objects.get_for_model(AdminUser)
    try:
        permission = Permission.objects.get(codename ='admin_permission2', content_type = ct)
    except:
        permission = Permission.objects.create(codename ='admin_permission2', content_type = ct)
    for i in user_for_permission:
        i.user_permissions.add(permission)

    photos = Gallery.objects.all()
    first_photo = Gallery.objects.all().first
    categories = CategoryGallery.objects.all()
    user = request.GET.get('user')
    password = request.GET.get('password')
    user_for_chat = None
    room = None
    room_messages = None
    admin_rooms = None
    admin_messages = None
    admin_room = None
    admin_media_for_messages = None
    admin_readable = None
    all_admin_readable = None
    if request.user.id:
        if request.user.user_type == "3":
            user_for_chat = CustomUser.objects.get(id=request.user.id)
    if user_for_chat:
        room = ChatRoom.objects.get(host=user_for_chat)
        room_messages = room.message_set.all().order_by('created')
    if request.user.is_authenticated:
        if request.user.user_type == "3":
            user_for_chat = CustomUser.objects.get(id=request.user.id)
            room = ChatRoom.objects.get(host=user_for_chat)
            room_messages = room.message_set.all().order_by('created') 
        if request.user.user_type == "1":
            admin_rooms = AdminChatRooms.objects.all()
            if request.GET.get('room_id'):
                room_id=request.GET['room_id']
                user_for_chat = CustomUser.objects.get(id=request.user.id)
                admin_messages = AdminChatMessage.objects.filter(room_id=room_id)
                admin_readable = AdminChatReadMessage.objects.filter(room_id=room_id, user_for_read=user_for_chat, is_read=0)
                all_admin_readable = AdminChatReadMessage.objects.filter(user_for_read=user_for_chat, is_read=0)
                admin_media_for_messages = AdminChatMessageMedia.objects.filter(message_id__in=admin_messages)
                admin_room = "Открыть комнату при открытии страницы"
            else:
                room_id="1"
                user_for_chat = CustomUser.objects.get(id=request.user.id)
                admin_messages = AdminChatMessage.objects.filter(room_id=room_id)
                admin_media_for_messages = AdminChatMessageMedia.objects.filter(message_id__in=admin_messages)
                admin_readable = AdminChatReadMessage.objects.filter(room_id=room_id, user_for_read=user_for_chat, is_read=0)
                all_admin_readable = AdminChatReadMessage.objects.filter(user_for_read=user_for_chat, is_read=0)
    return render (request, 'main_templates/home.html', {'photos':photos, 'first_photo':first_photo, 'categories':categories, 'user':user, 'password':password, 'room':room, 'room_messages':room_messages, 'admin_rooms':admin_rooms, 'admin_messages':admin_messages, "admin_room":admin_room, "admin_media_for_messages":admin_media_for_messages, "admin_readable":admin_readable, "all_admin_readable":all_admin_readable})    

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

from AppOko.models import CustomUser
#ADMIN FUNCTION
def adminLogin(request):
    return render(request,"admin_templates/signin.html")

def adminLoginProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    user=authenticate(request=request,username=username,password=password)
    if user is not None:
        user = CustomUser.objects.get(username=username)
        if user.user_type == '1':
            login(request=request, user=user, backend = 'django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse("home"))
        if user.user_type == '4':
            login(request=request, user=user, backend = 'AppOko.auth_backend.PasswordlessAuthBackend')
            # return render (request, 'main_templates/home.html', {'password': user.password})
            return HttpResponseRedirect(reverse("home"))
        if user.user_type == '3':
            login(request=request, user=user, backend = 'django.contrib.auth.backends.ModelBackend')
            return HttpResponseRedirect(reverse("home"))
    else:
        messages.error(request,"Ошибка в Логине")
        return HttpResponseRedirect(reverse("admin_login"))
    
def adminLogoutProcess(request):
    logout(request)
    # messages.success(request,"Вы успешло вышли")
    return HttpResponseRedirect(reverse("home"))

def adminRegistrationProcess(request):
    username=request.POST.get("username")
    password=request.POST.get("password")
    password2=request.POST.get("password2")
    if password == password2:
        if not request.user.is_authenticated:
            old_custom_user = CustomUser.objects.create(username=username)
            old_custom_user.user_type = '3'
            old_custom_user.is_staff = '0'
            old_custom_user.set_password(password)
            ChatRoom.objects.create(host=old_custom_user)
            old_custom_user.save()
            new_user = CustomerUser.objects.create(auth_user_id_id=old_custom_user.id)
            return HttpResponseRedirect(reverse("home"))
        if request.user.user_type != "4":
            user = CustomUser.objects.get(username=username)
            if user.user_type == '1':
                login(request=request, user=user, backend = 'django.contrib.auth.backends.ModelBackend')
                return HttpResponseRedirect(reverse("admin_home"))
            if user.user_type == '4':
                login(request=request, user=user, backend = 'AppOko.auth_backend.PasswordlessAuthBackend')
                return HttpResponseRedirect(reverse("home"))
            else:
                return HttpResponseRedirect(reverse("home"))
        else:
            old_custom_user = CustomUser.objects.get(username=request.user.username)
            old_tempcustomer_user = TempCustomerUser.objects.get(auth_user_id_id=old_custom_user.id)
            edit_project=Projects.objects.get(id=old_tempcustomer_user.project_id)
            old_tempcustomer_user.delete()
            old_custom_user.user_type = '3'
            old_custom_user.username = username
            old_custom_user.set_password(password)
            old_custom_user.save()
            new_user = CustomerUser.objects.create(auth_user_id_id=old_custom_user.id)
            new_user.save()
            edit_project.user=old_custom_user
            edit_project.save()
            return HttpResponseRedirect(reverse("home"))
    else:
        messages.error(request,"Не одинаковые пароли")
        return HttpResponseRedirect(reverse("home"))

def bukvy(request):
    return render (request, 'main_templates/bukvy.html',) 