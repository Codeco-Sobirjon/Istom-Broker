from django.db import models
from django.utils.translation import gettext as _
from django_ckeditor_5.fields import CKEditor5Field
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.account.models import CustomUser


class Category(models.Model):
    name = models.CharField(_("Название категория"), max_length=250, null=True, blank=True)  # Removed the comma here
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name="Родитель категории",
        related_name='subcategories'
    )
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    def __str__(self):
        str_name = self.name or _("Без названия")
        parent = self.parent

        while parent:
            parent_name = parent.name or _("Без названия")
            str_name = f'{parent_name} / ' + str_name
            parent = parent.parent

        return str_name


class TopLevelCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "1. Основная категория"
        verbose_name_plural = "1. Основная категория"


class SubCategory(Category):
    class Meta:
        proxy = True
        verbose_name = "2. Подкатегория"
        verbose_name_plural = "2. Подкатегория"


class Product(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название")
    price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2, verbose_name="Цена")
    discount_price = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2,
                                         verbose_name="Цена со скидкой")
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.CASCADE, verbose_name="Категория")
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Автор")
    brand = models.CharField(_("Бренд продукции"), max_length=250, null=True, blank=True)
    size = models.CharField(_("Размер"), max_length=250, null=True, blank=True)
    volume = models.CharField(_("Объём"), max_length=250, null=True, blank=True)
    size_of_brackets = models.CharField(_("Размер скоб"), max_length=250, null=True, blank=True)
    the_height_of_the_closing_barckets = models.CharField(_("Высота закрытия скобок"), max_length=250, null=True, blank=True)
    outer_diameter_of_the_head = models.CharField(_("Внешний диаметр головки (мм)"),
                                                  max_length=250, null=True, blank=True)
    firm = models.CharField(max_length=255, null=True, blank=True, verbose_name="Фирма")
    country = models.CharField(max_length=255, null=True, blank=True, verbose_name="Страна")
    vendor_code = models.CharField(max_length=255, null=True, blank=True, verbose_name="Артикул")
    degree_of_extensibility = models.CharField(max_length=255, null=True, blank=True, verbose_name="Степень расширяемости")
    color = models.CharField(max_length=255, null=True, blank=True, verbose_name="Цвет")
    description = CKEditor5Field(config_name='extends', null=True, blank=True, verbose_name="Краткое описание")
    is_discount = models.BooleanField(default=False, null=True, blank=True, verbose_name="Есть скидка")
    is_new_product = models.BooleanField(default=False, null=True, blank=True, verbose_name="Это новый продукт")
    in_stock = models.BooleanField(default=True, null=True, blank=True, verbose_name="В наличии")  # Indicates if the product is in stock
    created_at = models.DateField(auto_now_add=True, null=True, blank=True, verbose_name="Дата публикации")

    objects = models.Manager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("3. Продукт")
        verbose_name_plural = _("3. Продукт")


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE, verbose_name="Продукт")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    content = models.TextField(verbose_name="Комментарий")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата комментария")

    objects = models.Manager()

    def __str__(self):
        return f"Комментарий от {self.user} к {self.product.name}"

    class Meta:
        verbose_name = _("4. Комментарий")
        verbose_name_plural = _("4. Комментарии")


class Review(models.Model):
    product = models.ForeignKey(Product, related_name='reviews', on_delete=models.CASCADE, verbose_name="Продукт")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Рейтинг"
    )
    content = models.TextField(verbose_name="Отзыв", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")

    objects = models.Manager()

    def __str__(self):
        return f"Отзыв от {self.user} на {self.product.name}"

    class Meta:
        verbose_name = _("5. Отзыв")
        verbose_name_plural = _("5. Отзывы")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name="Продукт")
    image = models.ImageField(upload_to='product_images/', null=True, blank=True, verbose_name="Изображение")

    objects = models.Manager()

    def __str__(self):
        return f"{self.product.name} - {self.id}"

    class Meta:
        verbose_name = _("Изображение продукта")
        verbose_name_plural = _("Изображение продукта")


class ProductSize(models.Model):
    product = models.ForeignKey(Product, related_name='sizes', null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name="Продукт")
    size = models.CharField(max_length=250, null=True, blank=True, verbose_name="Размер")

    objects = models.Manager()

    def __str__(self):
        return f"{self.product.name} - {self.id}"

    class Meta:
        verbose_name = _("Размер продукта")
        verbose_name_plural = _("Размер продукта")


class OrderProduct(models.Model):
    STATUS_CHOICES = [
        ('payed', 'Оплачено'),
        ('processing', 'Не оплачено'),
    ]

    product = models.ForeignKey(Product, related_name='order_product', null=True, blank=True, on_delete=models.CASCADE,
                                verbose_name="Продукт", )
    quantity = models.IntegerField(default=0, null=True, blank=True, verbose_name="Количество")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing', verbose_name="Статус")
    total = models.IntegerField(default=0, null=True, blank=True, verbose_name="Общая стоимость")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, verbose_name="Пользователь",
                             related_name='order_user')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    objects = models.Manager()

    def __str__(self):
        return f"{self.product.name}"

    class Meta:
        verbose_name = _("6 Заказанный продукт")
        verbose_name_plural = _("6 Заказанные продукты")
