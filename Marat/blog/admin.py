from django.contrib import admin
from .models import Club, Post, Comment


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'founded', 'stadium')
    search_fields = ('name', 'country')
    list_filter = ('country', 'founded')
    readonly_fields = ('logo',)  # Логотип только для просмотра


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'club', 'author', 'date_posted')
    search_fields = ('title', 'content', 'author')
    list_filter = ('club', 'date_posted', 'author')
    readonly_fields = ('date_posted',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('subject', 'author', 'post', 'created_at', 'is_published')
    list_filter = ('is_published', 'created_at', 'post__club')
    search_fields = ('subject', 'author', 'text')
    readonly_fields = ('created_at',)
    actions = ['publish', 'unpublish']

    def publish(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"Опубликовано: {queryset.count()} комментариев.")
    publish.short_description = "Опубликовать"

    def unpublish(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"Снято с публикации: {queryset.count()} комментариев.")
    unpublish.short_description = "Снять с публикации"