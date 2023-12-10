from django.contrib import admin

from .models import Post, Comment


admin.site.register(Comment)



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created']
    list_filter = ['created', 'created', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    ordering = ['created',]

