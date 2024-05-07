from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class ProductCategory(models.Model):
    categories = models.ForeignKey(to="ProductCategory", on_delete=models.CASCADE,
                                   verbose_name=_("categories"), blank=True, null=True)
    title = models.CharField(max_length=200, db_index=True, verbose_name=_("title"))
    url_title = models.CharField(_("url title"), db_index=True, max_length=200)
    is_active = models.BooleanField(_("is active"), default=True)
    is_delete = models.BooleanField(_("is delete"), default=False)

    def __str__(self):
        return f"( {self.url_title} / {self.title} )"

    class Meta:
        db_table = "category"
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")


class Brand(models.Model):
    title = models.CharField(_("brand"), max_length=300)
    is_active = models.BooleanField(_("is active"), default=True)
    
    def __str__(self):
        return self.title
    

class Product(models.Model):
    title = models.CharField(_("title"), max_length=300)
    price = models.IntegerField(_("price"))
    count = models.PositiveIntegerField(default=1, verbose_name=_("count"))
    product_category = models.ManyToManyField(to=ProductCategory, verbose_name=_("product category"),
                                         related_name="product_categories")
    brands = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="products_brand",
                               verbose_name=_("products brand"), blank=True, null=True)
    short_description = models.CharField(_("short description"), max_length=500, null=True)
    description = models.TextField(_("description"))
    slug = models.SlugField(default='', null=False, unique=True, verbose_name=_("slug"))
    image = models.ImageField(_("image"), upload_to="product/%Y/%m/%d/", blank=True, null=True)
    is_active = models.BooleanField(default=True, verbose_name=_("is active"))
    is_delete = models.BooleanField(_("is delete"), default=False)

    class Meta:
        db_table = "product"
        verbose_name = _("product")
        verbose_name_plural = _("products")
        

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(viewname='product-detail', args=[self.slug])


class ProductTag(models.Model):
    caption = models.CharField(_("caption"), max_length=250, db_index=True)
    product_tags = models.ManyToManyField(Product,
                                          verbose_name=_("product tags"),
                                          related_name="product_tags")

    class Meta:
        db_table = "tag"
        verbose_name = _("product tag")
        verbose_name_plural = _("product tags")

    def __str__(self):
        return self.caption


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="product_gallery/")
    
    def __str__(self):
        return f"{self.product.title} {self.image}"
    