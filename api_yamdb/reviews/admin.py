from django.contrib import admin

from .models import Category, Comments, Genre, Review, Title


class TitleAdmin(admin.ModelAdmin):
    list_display = ('pk', 'category', 'name', 'year', 'description')
    list_display_links = ('name', 'description')
    list_editable = ('category',)
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'
    search_fields = ('name',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    list_editable = ('slug',)
    list_display_links = ('pk',)
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'title', 'text', 'pub_date', 'score')


class CommentsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'author', 'review', 'text', 'pub_date')


admin.site.register(Title, TitleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comments, CommentsAdmin)
