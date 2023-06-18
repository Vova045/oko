# Generated by Django 4.1.4 on 2023-06-18 22:37

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="AdminChatMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["updated", "created"],
            },
        ),
        migrations.CreateModel(
            name="AdminChatRooms",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("is_active", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Categories",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Наименование"),
                ),
                (
                    "url_slug",
                    models.CharField(max_length=255, verbose_name="URL-название"),
                ),
                (
                    "thumbnail",
                    models.FileField(
                        blank=True,
                        default="nofoto.jpeg",
                        null=True,
                        upload_to="",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                ("is_active", models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CategoryGallery",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("is_active", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Chapters",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Наименование"),
                ),
                ("url_slug", models.CharField(max_length=255, verbose_name="URL-имя")),
                (
                    "thumbnail",
                    models.FileField(
                        blank=True,
                        default="nofoto.jpeg",
                        null=True,
                        upload_to="",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                ("is_active", models.IntegerField(blank=True, default=1, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="ChatRoom",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-updated", "-created"],
            },
        ),
        migrations.CreateModel(
            name="CustomerOrder",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("purchase_price", models.CharField(max_length=255)),
                ("coupon_code", models.CharField(max_length=255)),
                ("discount_amt", models.CharField(max_length=255)),
                ("product_status", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="CustomerUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_pic",
                    models.FileField(blank=True, default="", null=True, upload_to=""),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="GuestList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ip", models.CharField(max_length=100, verbose_name="IP-адрес")),
                (
                    "time",
                    models.DateTimeField(
                        auto_now_add=True, null=True, verbose_name="Дата входа"
                    ),
                ),
                (
                    "count_ip",
                    models.PositiveIntegerField(
                        blank=True,
                        default=0,
                        null=True,
                        verbose_name="Количество посещений",
                    ),
                ),
                (
                    "last_time",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="Последний вход"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductReviews",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("review_image", models.FileField(upload_to="")),
                ("rating", models.CharField(default=5, max_length=255)),
                ("review", models.TextField(default="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="Products",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("url_slug", models.CharField(max_length=255)),
                ("article", models.CharField(max_length=255)),
                ("product_name", models.CharField(max_length=255)),
                ("size", models.CharField(default="0", max_length=255)),
                (
                    "product_max_price",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                (
                    "product_discount_price",
                    models.CharField(
                        blank=True, default=None, max_length=255, null=True
                    ),
                ),
                ("product_description", models.TextField(blank=True, null=True)),
                ("product_long_description", models.TextField(blank=True, null=True)),
                ("created_ad", models.DateTimeField(auto_now_add=True)),
                ("in_stock_total", models.BigIntegerField(default=1)),
                ("is_active", models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name="ProductVarient",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Projects",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("date", models.CharField(blank=True, max_length=150, null=True)),
                ("number", models.CharField(blank=True, max_length=150, null=True)),
                ("name", models.CharField(blank=True, max_length=150, null=True)),
                ("client", models.CharField(blank=True, max_length=150, null=True)),
                ("manager", models.CharField(blank=True, max_length=150, null=True)),
            ],
            options={
                "ordering": ["-number"],
            },
        ),
        migrations.CreateModel(
            name="CustomUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "user_type",
                    models.CharField(
                        choices=[
                            (1, "Admin"),
                            (2, "Staff"),
                            (3, "Customer"),
                            (4, "TempCustomer"),
                        ],
                        default=1,
                        max_length=255,
                    ),
                ),
                ("is_staff", models.IntegerField(blank=True, default=1, null=True)),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="TempCustomerUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_pic",
                    models.FileField(blank=True, default="", null=True, upload_to=""),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "auth_user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "project",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="AppOko.projects",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="SubCategories",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Наименование"),
                ),
                (
                    "url_slug",
                    models.CharField(max_length=255, verbose_name="URL-название"),
                ),
                (
                    "thumbnail",
                    models.FileField(
                        blank=True,
                        default="nofoto.jpeg",
                        null=True,
                        upload_to="",
                        verbose_name="Картинка",
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                ("created_ad", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(blank=True, default=1, null=True)),
                (
                    "category",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="AppOko.categories",
                        verbose_name="Категория",
                    ),
                ),
                (
                    "chapter_id",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="AppOko.chapters",
                        verbose_name="Раздел",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StaffUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "profile_pic",
                    models.FileField(blank=True, default="", null=True, upload_to=""),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "auth_user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="projects",
            name="user",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.CreateModel(
            name="ProductVarientItem",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
                (
                    "product_varient_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.productvarient",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductTransaction",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("transaction_product_count", models.IntegerField(default=1)),
                (
                    "transaction_type",
                    models.CharField(choices=[(1, "BUY"), (2, "SELL")], max_length=255),
                ),
                ("transaction_description", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductTags",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="products",
            name="added_by_staff",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="AppOko.staffuser",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="categories_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="AppOko.categories",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="chapters_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="AppOko.chapters",
            ),
        ),
        migrations.AddField(
            model_name="products",
            name="subcategories_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="AppOko.subcategories",
            ),
        ),
        migrations.CreateModel(
            name="ProductReviewVoting",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
                (
                    "product_review_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.productreviews",
                    ),
                ),
                (
                    "user_id_voting",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.customeruser",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="productreviews",
            name="product_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="AppOko.products"
            ),
        ),
        migrations.AddField(
            model_name="productreviews",
            name="user_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="AppOko.customeruser"
            ),
        ),
        migrations.CreateModel(
            name="ProductQuestions",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("question", models.TextField()),
                ("answer", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
                (
                    "user_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.customeruser",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductMedia",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("media_type", models.CharField(max_length=255)),
                ("media_content", models.FileField(upload_to="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductDetails",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("title_details", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductAbout",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.IntegerField(default=1)),
                (
                    "product_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.products",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderDeliveryStatus",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("status", models.CharField(max_length=255)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now_add=True)),
                (
                    "order_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.customerorder",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Message",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.TextField()),
                ("updated", models.DateTimeField(auto_now=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.chatroom",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "ordering": ["updated", "created"],
            },
        ),
        migrations.CreateModel(
            name="Gallery",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("title", models.CharField(max_length=255)),
                ("media_content", models.FileField(upload_to="")),
                (
                    "description",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("customer", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "order_number",
                    models.CharField(blank=True, max_length=255, null=True),
                ),
                ("is_active", models.IntegerField(default=1)),
                (
                    "type_of_product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.categorygallery",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="customeruser",
            name="auth_user_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="customeruser",
            name="project",
            field=models.OneToOneField(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="AppOko.projects",
            ),
        ),
        migrations.AddField(
            model_name="customerorder",
            name="product_id",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="AppOko.products"
            ),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="host",
            field=models.OneToOneField(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="chatroom",
            name="participants",
            field=models.ManyToManyField(
                blank=True, related_name="participants", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddField(
            model_name="categories",
            name="chapter_id",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="AppOko.chapters",
                verbose_name="Раздел",
            ),
        ),
        migrations.CreateModel(
            name="AdminUser",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("profile_pic", models.FileField(default="", upload_to="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "auth_user_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdminChatReadMessage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("is_read", models.IntegerField(default=0)),
                (
                    "message_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.adminchatmessage",
                    ),
                ),
                (
                    "room",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.adminchatrooms",
                    ),
                ),
                (
                    "user_for_read",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AdminChatMessageMedia",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("media_content", models.FileField(upload_to="")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "message_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="AppOko.adminchatmessage",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="adminchatmessage",
            name="room",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="AppOko.adminchatrooms"
            ),
        ),
        migrations.AddField(
            model_name="adminchatmessage",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
