from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.urls import reverse

class CustomUser(AbstractUser):
    user_type_choices=((1,"Admin"),(2,"Staff"),(3,"Customer"),(4,"TempCustomer"),)
    user_type=models.CharField(max_length=255,choices=user_type_choices, default=1)
    is_staff = models.IntegerField(null=True, blank=True, default=1)


class Projects (models.Model):
    date = models.CharField(max_length=150,null=True, blank=True)
    number = models.CharField(max_length=150,null=True, blank=True)
    name = models.CharField(max_length=150,null=True, blank=True)
    client = models.CharField(max_length=150,null=True, blank=True)
    manager = models.CharField(max_length=150,null=True, blank=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.number

    class Meta:
        ordering = ['-number']


class AdminUser(models.Model):
    profile_pic=models.FileField(default="")
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)


class StaffUser(models.Model):
    profile_pic=models.FileField(default="", blank=True, null=True)
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)

class CustomerUser(models.Model):
    profile_pic=models.FileField(default="", blank=True, null=True)
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    project = models.OneToOneField(Projects, on_delete=models.SET_NULL, blank=True, null=True)

class TempCustomerUser(models.Model):
    profile_pic=models.FileField(default="", blank=True, null=True)
    auth_user_id=models.OneToOneField(CustomUser,on_delete=models.PROTECT)
    created_at=models.DateTimeField(auto_now_add=True)
    project = models.OneToOneField(Projects,on_delete=models.SET_NULL, blank=True, null=True)

class Chapters(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, verbose_name='Наименование')
    url_slug=models.CharField(max_length=255, verbose_name='URL-имя')
    thumbnail=models.FileField(null=True, blank=True, default='nofoto.jpeg', verbose_name='Картинка')
    description=models.TextField(null=True, blank=True, verbose_name='Описание')
    is_active=models.IntegerField(null=True, blank=True, default=1)

    def get_absolute_url(self):
        return reverse("chapter_list")

    def __str__(self):
        return self.title

class Categories(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255, verbose_name='Наименование')
    url_slug=models.CharField(max_length=255, verbose_name='URL-название')
    thumbnail=models.FileField(null=True, blank=True, default='nofoto.jpeg', verbose_name='Картинка')
    description=models.TextField(null=True, blank=True, verbose_name='Описание')
    is_active=models.IntegerField(null=True, blank=True, default=1)
    chapter_id=models.ForeignKey(Chapters, on_delete=models.PROTECT,null=True, blank=True, verbose_name='Раздел')

    def get_absolute_url(self):
        return reverse("category_list") 

    def __str__(self):
        return self.title

class SubCategories(models.Model):
    id=models.AutoField(primary_key=True)
    chapter_id=models.ForeignKey(Chapters, on_delete=models.PROTECT,null=True, blank=True, verbose_name='Раздел')
    title=models.CharField(max_length=255, verbose_name='Наименование')
    url_slug=models.CharField(max_length=255, verbose_name='URL-название')
    thumbnail=models.FileField(null=True, blank=True, default='nofoto.jpeg', verbose_name='Картинка')
    description=models.TextField(null=True, blank=True, verbose_name='Описание')
    created_ad=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(null=True, blank=True, default=1)
    category = models.ForeignKey(Categories, on_delete=models.PROTECT, blank=True, null=True, verbose_name='Категория')

    def get_absolute_url(self):
        return reverse("sub_category_list") 

    def __str__(self):
        return self.title


class Products(models.Model):
    id=models.AutoField(primary_key=True)
    url_slug=models.CharField(max_length=255)
    article=models.CharField(max_length=255)
    subcategories_id=models.ForeignKey(SubCategories,on_delete=models.PROTECT, null=True, blank=True)
    categories_id=models.ForeignKey(Categories,on_delete=models.PROTECT, null=True, blank=True)
    chapters_id=models.ForeignKey(Chapters,on_delete=models.PROTECT, null=True, blank=True)
    product_name=models.CharField(max_length=255)
    size=models.CharField(max_length=255, default='0')
    product_max_price=models.CharField(max_length=255, null=True, blank=True)
    product_discount_price=models.CharField(max_length=255, null=True, blank=True, default=None)
    product_description=models.TextField(null=True, blank=True)
    product_long_description=models.TextField(null=True, blank=True)
    created_ad=models.DateTimeField(auto_now_add=True)
    added_by_staff=models.ForeignKey(StaffUser, on_delete=models.PROTECT, blank=True, null=True)
    in_stock_total = models.BigIntegerField(default=1)
    is_active=models.IntegerField(default=1)

class ProductMedia(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    media_type_choice=((1,"Image"),(2,"Video"))
    media_type=models.CharField(max_length=255)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductTransaction(models.Model):
    id=models.AutoField(primary_key=True)
    transaction_type_choices=((1, "BUY"),(2,"SELL"))
    product_id=models.ForeignKey(Products, on_delete=models.CASCADE)
    transaction_product_count=models.IntegerField(default=1)
    transaction_type=models.CharField(choices=transaction_type_choices,max_length=255)
    transaction_description=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductDetails(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    title_details=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductAbout(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductTags(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductQuestions(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    question=models.TextField()
    answer=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviews(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    user_id=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    review_image=models.FileField()
    rating=models.CharField(default=5, max_length=255)
    review=models.TextField(default="")
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductReviewVoting(models.Model):
    id=models.AutoField(primary_key=True)
    product_review_id=models.ForeignKey(ProductReviews,on_delete=models.CASCADE)
    user_id_voting=models.ForeignKey(CustomerUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    is_active=models.IntegerField(default=1)

class ProductVarient(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class ProductVarientItem(models.Model):
    id=models.AutoField(primary_key=True)
    product_varient_id=models.ForeignKey(ProductVarient, on_delete=models.CASCADE)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    title=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class CustomerOrder(models.Model):
    id=models.AutoField(primary_key=True)
    product_id=models.ForeignKey(Products,on_delete=models.CASCADE)
    purchase_price=models.CharField(max_length=255)
    coupon_code=models.CharField(max_length=255)
    discount_amt=models.CharField(max_length=255)
    product_status=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)

class OrderDeliveryStatus(models.Model):
    id=models.AutoField(primary_key=True)
    order_id=models.ForeignKey(CustomerOrder, on_delete=models.CASCADE)
    status=models.CharField(max_length=255)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender,instance,created,**kwards):
    if created:
        if instance.user_type==1:
            AdminUser.objects.create(auth_user_id=instance)
        if instance.user_type==2:
            StaffUser.objects.create(auth_user_id=instance)
        if instance.user_type==3:
            CustomerUser.objects.create(auth_user_id=instance) 
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance, **kwargs):
    if instance.user_type==1:
        instance.adminuser.save()
    if instance.user_type==2:
        instance.staffuser.save()
    if instance.user_type==3:
        instance.customeruser.save()

#Просмотры и Гости

class GuestList(models.Model):
    ip = models.CharField('IP-адрес', max_length=100)
    time = models.DateTimeField(verbose_name="Дата входа", auto_now_add=True, null=True)
    count_ip = models.PositiveIntegerField(verbose_name='Количество посещений', null = True, default=0, blank=True)
    last_time = models.DateTimeField(verbose_name='Последний вход', blank=True, null=True)

    def __str__(self):
        return self.ip

    def get_absolute_url(self):
        return reverse("guest_list")

class CategoryGallery(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    is_active=models.IntegerField(default=1)

class Gallery(models.Model):
    id=models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    type_of_product = models.ForeignKey(CategoryGallery, on_delete=models.CASCADE, blank=True, null=True)
    media_content = models.FileField()
    description = models.CharField(max_length=255, blank=True, null=True)
    customer = models.CharField(max_length=255, blank=True, null=True)
    order_number = models.CharField(max_length=255, blank=True, null=True)
    is_active=models.IntegerField(default=1)


    def get_absolute_url(self):
        return reverse("gallery_list")    

class ChatRoom(models.Model):
    host = models.OneToOneField(CustomUser, on_delete=models.SET_NULL, null=True)
    participants = models.ManyToManyField(CustomUser, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.host

class Message(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.body[0:50]

class AdminChatRooms(models.Model):
    name = models.CharField(max_length=255)
    is_active=models.IntegerField(default=1)

class AdminChatMessage(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(AdminChatRooms, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['updated', 'created']

    def __str__(self):
        return self.body[0:50]

class AdminChatMessageMedia(models.Model):
    message_id=models.ForeignKey(AdminChatMessage,on_delete=models.CASCADE)
    media_content=models.FileField()
    created_at=models.DateTimeField(auto_now_add=True)

# class AdminParticipants(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     room = models.ForeignKey(AdminChatRooms, on_delete=models.CASCADE)

class AdminChatReadMessage(models.Model):
    message_id=models.ForeignKey(AdminChatMessage,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read=models.IntegerField(default=0)
    user_for_read = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    room = models.ForeignKey(AdminChatRooms, on_delete=models.CASCADE)
    




