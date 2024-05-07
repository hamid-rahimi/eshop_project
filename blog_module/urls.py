from django.urls import path
from . import views

app_name = 'blog_module'
urlpatterns = [
    path("", views.BlogListView.as_view(), name="blog_list_page"),
    path("<int:category_id>/", views.BlogListView.as_view(), name="blog_list_page"),
#     path('main/category/<int:category_id>/', get_list_by_category, name="category_page"),
#     path('main/author/<int:author_id>/', get_list_by_author, name="author_page"),
    path("detail/<slug:slug>/", views.BlogDetailView.as_view(), name="blog_detail_page"),
    path("submit-comment/", views.submit_comment, name="submit_comment"),
#     path("update/<int:article_id>/", update_page, name="update_page"),
#     path("delete/<int:article_id>/", delete_page, name="delete_page"),
#     path("article/", add_article, name="add_article"),
#     path("person/", add_person, name="add_person"),
    
    # path("update/<int:pk>/", update_page, name="update_page"),
]
