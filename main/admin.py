from django.contrib import admin
from .models import (
    TeamMember, Project, ProjectFeature,
    ProjectTechStack, SocialLink, Service, Publication, ProjectResultImage, News
)


class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
    fields = ('icon_class', 'url')


class PublicationInline(admin.StackedInline):
    model = Publication
    extra = 0
    fields = (
        ('title_ru', 'title_kk', 'title_en'),
        'source',
        'publication_date',
        ('description_ru', 'description_kk', 'description_en'),
        'url',
        'project'
    )
    autocomplete_fields = ['project']


class ProjectResultImageInline(admin.TabularInline):
    model = ProjectResultImage
    extra = 1
    fields = ('image', 'caption_ru', 'caption_kk', 'caption_en')


class ProjectFeatureInline(admin.TabularInline):
    model = ProjectFeature
    extra = 1
    fields = ('icon_class', 'text_ru', 'text_kk', 'text_en', 'order')


class ProjectTechStackInline(admin.TabularInline):
    model = ProjectTechStack
    extra = 1
    fields = ('icon_class', 'text', 'order')


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name_ru', 'position_ru', 'is_visible')
    search_fields = ('name_ru', 'name_kk', 'name_en')
    prepopulated_fields = {'slug': ('name_ru',)}

    list_editable = ('is_visible',)

    fieldsets = (
        ('Фото и URL', {
            'fields': ('photo', 'slug')
        }),
        ('ФИО (3 языка)', {
            'fields': ('name_ru', 'name_kk', 'name_en')
        }),
        ('Должность (3 языка)', {
            'fields': ('position_ru', 'position_kk', 'position_en')
        }),
        ('Биография', {
            'fields': ('bio_ru', 'bio_kk', 'bio_en'),
            'classes': ('collapse',),
        }),
        ('Научные идентификаторы', {
            'fields': ('scopus_id', 'orcid_id')
        }),
    )
    inlines = [SocialLinkInline, PublicationInline]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'category', 'slug')
    list_filter = ('category',)
    prepopulated_fields = {'slug': ('title_ru',)}
    filter_horizontal = ('team',)
    inlines = [ProjectFeatureInline, ProjectTechStackInline, ProjectResultImageInline]
    search_fields = ('title_ru', 'keywords')

    fieldsets = (
        ('Основная информация', {
            'fields': (
                'category', 'slug', 'external_link', 'keywords',
                'title_ru', 'title_kk', 'title_en',
                'tagline_ru', 'tagline_kk', 'tagline_en',
            )
        }),
        ('Статусы', {
            'fields': (
                ('status_tag_1_ru', 'status_tag_1_kk', 'status_tag_1_en'),
                ('status_tag_2_ru', 'status_tag_2_kk', 'status_tag_2_en'),
            )
        }),
        ('Полное описание', {
            'fields': ('full_description_ru', 'full_description_kk', 'full_description_en'),
            'classes': ('collapse',),
        }),
        ('Задачи и Результаты', {
            'fields': (
                'task_description_ru', 'task_description_kk', 'task_description_en',
                'task_subtitle_ru', 'task_subtitle_kk', 'task_subtitle_en',
                'result_description_ru', 'result_description_kk', 'result_description_en',
            ),
            'classes': ('collapse',),
        }),
        ('Дополнительно', {
            'fields': ('detailed_info_ru', 'detailed_info_kk', 'detailed_info_en'),
            'classes': ('collapse',),
        }),
        ('Команда', {
            'fields': ('team',)
        }),
    )


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'category', 'published_date', 'project', 'author_name')
    list_filter = ('category', 'published_date', 'project')
    search_fields = ('title_ru', 'content_ru', 'keywords')
    prepopulated_fields = {'slug': ('title_ru',)}
    autocomplete_fields = ['project']

    fieldsets = (
        (None, {
            'fields': ('slug', 'category', 'project', 'author_name', 'published_date', 'image')
        }),
        ('Заголовок (3 языка)', {
            'fields': ('title_ru', 'title_kk', 'title_en')
        }),
        ('Контент (3 языка)', {
            'fields': ('content_ru', 'content_kk', 'content_en')
        }),
        ('SEO', {
            'fields': ('keywords',)
        }),
    )


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title_ru', 'order')
    list_editable = ('order',)
    fieldsets = (
        (None, {
            'fields': ('icon_class', 'order')
        }),
        ('Название (3 языка)', {
            'fields': ('title_ru', 'title_kk', 'title_en')
        }),
        ('Описание (3 языка)', {
            'fields': ('description_ru', 'description_kk', 'description_en')
        }),
    )