from django.contrib import admin
from django.contrib.admin import AdminSite
from .models import Category, Post, Comment

# Custom admin site header
AdminSite.site_header = "Prateek's Blog Administration"
AdminSite.site_title = "Prateek's Blog Admin"
AdminSite.index_title = "Welcome to Prateek's Blog Admin Panel"

# PROFILE SECTION REMOVED - Delete the entire @admin.register(Profile) block

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'post_count']
    search_fields = ['name']
    
    def post_count(self, obj):
        return obj.post_set.count()
    post_count.short_description = 'Posts'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'published_date', 'comment_count']
    list_filter = ['category', 'published_date', 'author']
    search_fields = ['title', 'content', 'author__username']
    date_hierarchy = 'published_date'
    readonly_fields = ['created_date']
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'content_preview', 'created_date', 'approved']
    list_filter = ['approved', 'created_date']
    search_fields = ['author__username', 'content', 'post__title']
    actions = ['approve_comments']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = 'Content Preview'
    
    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
    approve_comments.short_description = "Approve selected comments"