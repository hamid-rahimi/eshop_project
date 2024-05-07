from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.http import HttpResponse, HttpRequest, JsonResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count
from django.contrib.auth import get_user_model

from . import models
from . import forms
from home_module.models import AdvertisingBanner

User = get_user_model()
article_selected_id = 0


class BlogListView(generic.ListView):
    model = models.Article
    template_name = "blog_module/index.html"
    context_object_name = 'articles'
    queryset = model.objects.filter(is_show=True)
    paginate_by = 1
    
    def get_context_data(self, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)

        context["categories"] = models.Category.objects.filter(is_active=True, parent=None)
        
        context['banners'] = AdvertisingBanner.objects.filter(location__iexact="blog_list_page")
        
        return context
    
    def get_queryset(self):
        query =  super().get_queryset()
        category_id = self.kwargs.get('category_id')
        if category_id:
            query = query.filter(categories__id=category_id, is_show=True)
        return query

    
class BlogDetailView(generic.DetailView):
    model = models.Article
    template_name = "blog_module/detail.html"
    template_name_field = 'article'
    
    def get_context_data(self, *args, **kwargs) -> dict:
        context = super().get_context_data(*args, **kwargs)
        article = kwargs.get('object')
        context["comments"] = models.Comment.objects.filter(article=article.id, status='published',
                                                            parent=None).order_by('-created_time').prefetch_related('replies')
        context['comments_count'] = models.Comment.objects.filter(status='published',
                                                            article=article.id).count()
        # avatar = models.Comment.objects.filter(author__userprofile__avatar__isnull=False)
        # print(context, self.kwargs, avatar)
        return context
    
def submit_comment(request:HttpRequest):
    print(request.GET)
    if request.user.is_authenticated:
        comment = request.GET.get('comment')
        article_selected_id = request.GET.get('article_id')
        article = get_object_or_404(models.Article, id=article_selected_id)
        parent_id = request.GET.get('parent_id')
        if parent_id.isdigit():
            parent = get_object_or_404(models.Comment, id=parent_id)
        else:
            parent = None
        author = request.user
        models.Comment.objects.create(body=comment, author=author, article=article, parent=parent)
        context = {
            'comments' : models.Comment.objects.filter(article=article_selected_id, status='published',
                                                        parent=None).order_by('-created_time').prefetch_related('replies'),
            'comments_count' : models.Comment.objects.filter(status='published',
                                                        article=article_selected_id).count()
        }
        return render(request, "blog_module/includes/inbox-reload-comment.html", context)
    
    # if request.user.is_authenticated:
    #     if request.method == 'POST' and request.headers.get('X-Requested-With') == 'AjaxRequest':
    #         message = request.POST.get('message')
    #         print(message)
    #         author = request.user
    #         article_selected_id = request.POST.get('article_id')
    #         article = get_object_or_404(models.Article, id=article_selected_id)
    #         comment = models.Comment.objects.create(
    #             body=message, author=author, article=article, title='test title')
    #         return JsonResponse({"success": True, "message": "نظر شما با موفقیت ثبت شد."})
    #     return JsonResponse({"success": False, "message": "خطا در ارسال نظر."})


def blog_page(request):
    article = Article.objects.all()
    authors = User.objects.all()
    categories = Category.objects.all()
    count_of_category = Category.objects.annotate(Count('article'))
    count_of_article_per_author = User.objects.annotate(Count('article'))
    # a=Article.categories.field_name
    # print(count_of_article_per_author)
    # print(a)
    # print('++++++')
    search_key = request.GET.get("search_title")
    # print(request.GET.get('search_text'), 11)
    if search_key:
        article = article.filter(title__icontains=search_key)
        
    paginator = Paginator(article, 6)
    num_page = request.GET.get('page')
    page_obj = paginator.get_page(num_page)

    context = {
        'articles': page_obj,
        'authors': authors,
        's_key': search_key,
        'categories': categories,
        'count_of_category': count_of_category,
        'count_of_article_per_author': count_of_article_per_author,
    }
    return render(request, "blog/index.html", context)

def detail_page(request, article_id):
    if request.method == 'post':
        article_selected_id = request.POST.id
        
    a = get_object_or_404(Article, id=article_id)
    article_selected_id = article_id
    context = {
        'article': a,
    }
    return render(request, "blog/details.html", context)

@login_required
def add_article(request):
    if request.user.is_authenticated:
        # print(request.method)
        if request.method == 'GET':
            form = CreateArticle()
        else:
            form = CreateArticle(data=request.POST, files=request.FILES)
            print(f"is valid: {form.is_valid()}")
            if form.is_valid():
                # print(form.cleaned_data)
                article_title = form.cleaned_data.get('title')
                article_text = form.cleaned_data['text']
                article_created_date = form.cleaned_data['created_date']
                article_is_show = form.cleaned_data['is_show']
                article_image = form.cleaned_data['image']
                # article_author = form.cleaned_data['author']
                # item = Person.objects.get(pk=article_author)
                Article.objects.create(title=article_title,
                                       text=article_text, created_date=article_created_date,                                   is_show=article_is_show,
                                       image=article_image,
                                       author=request.user
                                    )
                a = Article.objects.last().pk
                # print(f"last item is: {a}")
                return redirect('blog:detail_page', a)

        context = {
            'form': form,
        }
        return render(request, "blog/add_article.html", context)
    else:
        return redirect('accounts:login_page')

@login_required
def add_person(request):
    if request.method == 'GET':
        # print(request.method)
        form_add = AddPerson()
    else:
        # print(request.method)
        form_add = AddPerson(data=request.POST)
        if form_add.is_valid():
            # print(f"is valid: {form_add.is_valid()}")
            # print(form_add.cleaned_data)
            person_fname = form_add.cleaned_data.get('first_name')
            person_lname = form_add.cleaned_data.get('last_name')
            person_age = form_add.cleaned_data.get('age')
            person_email = form_add.cleaned_data.get('email')
            P = Person.objects.create(
                first_name=person_fname,
                last_name=person_lname,
                age=person_age,
                email=person_email
            )
            return redirect("blog:blog_page")

    return render(request, "blog/add_person.html", {'form': form_add})

@login_required
def update_page(request, article_id):
    record = get_object_or_404(Article, id=article_id)
    # print(request.user.id)
    # print(record.author.id)
    if request.user.id != record.author.id:
        return HttpResponse(f"page error.../{request.user}/{record.author}")
    if request.method == 'GET':
        # print(record)
        article_form = UpdateArticle(initial={
            'title' : record.title,
            'text' : record.text,
            'created_date' : record.created_date,
            'is_show' : record.is_show,
            # 'imag' : record.image,
            })
    else:
        article_form = UpdateArticle(data=request.POST, files=request.FILES)
        if article_form.is_valid():
            title = article_form.cleaned_data.get('title')
            text = article_form.cleaned_data.get('text')
            # created_date = article_form.cleaned_data.get('created_date')
            is_show = article_form.cleaned_data.get('is_show')
            image = article_form.cleaned_data.get('image')
            
            record.title = title
            record.text = text
            # record.crated_date = created_date
            record.is_show = is_show
            if image:
                record.image = image
            
            record.save()
            
            return redirect('blog:detail_page', article_id)
    context = {'form' : article_form, 'edit' : record}
            
    return render(request, 'blog/edit_article.html', context)

@login_required
def delete_page(request, article_id):
    record = get_object_or_404(Article, pk=article_id)
    if request.user.id != record.author.id:
        return HttpResponse("page error...")
    record.delete()
    return redirect('blog:blog_page')

def get_list_by_category(request, category_id):
    articles = Article.objects.filter(categories=category_id)
    categories = Category.objects.all()
    count_of_category = Category.objects.annotate(Count('article'))
    
    paginator = Paginator(object_list=articles, per_page=3)
    num_page = request.GET.get('page')
    page_obj = paginator.get_page(number=num_page)
    
    context = {
        'articles': page_obj,
        'categories': categories,
        'count_of_category': count_of_category,
    }
    return render(request, "blog\index.html", context)

def get_list_by_author(request, author_id):
    articles = Article.objects.filter(author__id=author_id)
    # print(articles)
    authors = User.objects.all()
    count_of_article_per_author = User.objects.annotate(Count('article'))
    
    paginator = Paginator(object_list=articles, per_page=3)
    num_page = request.GET.get('page')
    page_obj = paginator.get_page(number=num_page)
    
    context = {
        'articles':page_obj,
        'authors':authors,
        'count_of_article_per_author':count_of_article_per_author,
    }
    return render(request=request, template_name='blog/index.html', context=context)