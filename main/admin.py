# main/admin.py

from django.contrib import admin
from .models import (
    TeamMember, Project, Icon, ProjectFeature,
    ProjectTechStack, SocialLink, Service, Publication, ProjectResultImage, News
)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
class PublicationInline(admin.StackedInline):
    model = Publication
    extra = 1
    fields = ('title', 'source', 'publication_date', 'description', 'url', 'project')
    autocomplete_fields = ['project']
class ProjectResultImageInline(admin.TabularInline):
    model = ProjectResultImage
    extra = 1
    fields = ('image', 'caption')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position')
    search_fields = ('name', 'position')
    prepopulated_fields = {'slug': ('name',)}
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'slug', 'position', 'photo', 'bio')
        }),
        ('Научные идентификаторы', {
            'fields': ('scopus_id', 'orcid_id')
        }),
    )
    inlines = [SocialLinkInline, PublicationInline]


@admin.register(Icon)
class IconAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon_class')
    search_fields = ('title', 'icon_class')

class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ('icon', 'text', 'order')

class ProjectTechStackInline(admin.TabularInline):
    model = ProjectTechStack
    extra = 1
    fields = ('icon', 'text', 'order')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('team',)
    inlines = [ProjectFeatureInline, ProjectTechStackInline, ProjectResultImageInline]
    search_fields = ('title', 'keywords')
    fieldsets = (
        ('Основная информация', {
            'fields': ('category', 'title', 'slug', 'tagline', 'status_tag_1', 'status_tag_2', 'external_link', 'keywords')
        }),
        ('Детальное описание', {
            'fields': ('full_description', 'task_description','task_subtitle', 'result_description', 'detailed_info')
        }),
        ('Команда', {
            'fields': ('team',)
        }),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'published_date', 'project', 'author_name')
    list_filter = ('category', 'published_date', 'project', 'author_name')
    search_fields = ('title', 'content', 'keywords')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['project']
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'category', 'project', 'author_name')
        }),
        ('Контент', {
            'fields': ('image', 'content', 'keywords')
        }),
        ('Даты', {
            'fields': ('published_date',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'order')
    list_editable = ('order',)
    autocomplete_fields = ['icon']