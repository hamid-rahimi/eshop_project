from django.contrib import admin
from . import models

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'is_active', )
    
class CommentAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'article', 'status', 'created_time', 'get_parent_title')

    def get_parent_title(self, obj):
        return obj.parent.title if obj.parent else '-'
    get_parent_title.short_description = 'عنوان والد'
    
    

admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Article)
# admin.site.register(Person)
admin.site.register(models.Category, CategoryAdmin)

