from random import randint
from django.contrib.auth import get_user_model
from django.db import models, transaction
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from model_utils import Choices
from model_utils.fields import StatusField   
from django.urls import reverse


User = get_user_model()

class Category(models.Model):
    parent = models.ForeignKey("self", blank=True, null=True,
                                     verbose_name="والد", on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    is_active = models.BooleanField(default=True)
    created_time = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, allow_unicode=True, db_index=True)
    
    def __str__(self):
        return self.title
    
    @transaction.atomic
    def save(self, *args, **kwargs):
        main_slug = slugify(self.title, allow_unicode=True).lower()
        while Category.objects.filter(slug=main_slug).exists():
            rand_int = randint(101, 1000)
            main_slug = f"{main_slug}-{rand_int}"
        self.slug = main_slug
        super().save(*args, **kwargs)
    
class Article(models.Model):
    STATUS = Choices('draft', 'published', 'hidden', 'archived', 'deleted')
    status = StatusField(choices=STATUS, default='draft', editable=True)
    
    categories = models.ManyToManyField(to='Category')
    title = models.CharField(max_length=250)
    short_description = models.CharField(max_length=500)
    text = models.TextField()
    created_time = models.DateTimeField(auto_now_add=True)
    is_show = models.BooleanField(default=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='blog/article/%Y/%m/')
    slug = AutoSlugField(populate_from=['title', 'author'], unique=True, allow_unicode=True, db_index=True)
    
    class Meta:
        index_together = [['slug', 'created_time']]
    
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(viewname='blog_module:blog_detail_page', args=(self.slug,))

class Comment(models.Model):
    STATUS = Choices('draft', 'published', 'hidden', 'archived', 'deleted')
    status = StatusField(choices=STATUS, default='published')
    # status = models.CharField(choices=STATUS, max_length=10, default='published')
    parent = models.ForeignKey("self", blank=True, null=True,
                               on_delete=models.CASCADE, related_name='replies')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comments')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments')
    title = models.CharField(max_length=250)
    created_time = models.DateTimeField(auto_now_add=True)
    body = models.TextField()
    
    def __str__(self):
        return f"comment by {self.author} => {self.title}"
    