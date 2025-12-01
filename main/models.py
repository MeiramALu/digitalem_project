from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import get_language


class TranslatableModel(models.Model):
    class Meta:
        abstract = True

    def get_tr(self, field_prefix):
        lang = get_language()
        val = getattr(self, f"{field_prefix}_{lang}", None)
        if not val:
            val = getattr(self, f"{field_prefix}_ru", None)
        return val


class Publication(TranslatableModel):
    member = models.ForeignKey('TeamMember', related_name='publications', on_delete=models.CASCADE,
                               verbose_name="Сотрудник")

    title_ru = models.CharField(max_length=255, verbose_name="Название статьи (RU)")
    title_kk = models.CharField(max_length=255, verbose_name="Название статьи (KK)", blank=True)
    title_en = models.CharField(max_length=255, verbose_name="Название статьи (EN)", blank=True)

    source = models.CharField(max_length=200, verbose_name="Журнал или источник")
    publication_date = models.DateField(verbose_name="Дата публикации")

    description_ru = RichTextUploadingField(verbose_name="Краткое описание (RU)", blank=True)
    description_kk = RichTextUploadingField(verbose_name="Краткое описание (KK)", blank=True)
    description_en = RichTextUploadingField(verbose_name="Краткое описание (EN)", blank=True)

    url = models.URLField(verbose_name="Ссылка на публикацию", blank=True)
    project = models.ForeignKey('Project', related_name='publications', on_delete=models.SET_NULL, null=True,
                                blank=True, verbose_name="Связанный проект")

    @property
    def title(self): return self.get_tr('title')

    @property
    def description(self): return self.get_tr('description')

    def __str__(self): return self.title_ru

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-publication_date', 'title_ru']


class TeamMember(TranslatableModel):
    is_visible = models.BooleanField(default=True, verbose_name="Отображать на сайте?")

    name_ru = models.CharField(max_length=100, verbose_name="Имя и Фамилия (RU)")
    name_kk = models.CharField(max_length=100, verbose_name="Имя и Фамилия (KK)", blank=True)
    name_en = models.CharField(max_length=100, verbose_name="Имя и Фамилия (EN)", blank=True)

    slug = models.SlugField(max_length=100, unique=True)

    position_ru = models.CharField(max_length=100, verbose_name="Должность (RU)", blank=True)
    position_kk = models.CharField(max_length=100, verbose_name="Должность (KK)", blank=True)
    position_en = models.CharField(max_length=100, verbose_name="Должность (EN)", blank=True)

    bio_ru = RichTextUploadingField(verbose_name="Биография (RU)", blank=True)
    bio_kk = RichTextUploadingField(verbose_name="Биография (KK)", blank=True)
    bio_en = RichTextUploadingField(verbose_name="Биография (EN)", blank=True)

    photo = models.ImageField(upload_to='team_photos/', verbose_name="Фотография")
    scopus_id = models.CharField(max_length=50, blank=True, verbose_name="Scopus Author ID")
    orcid_id = models.CharField(max_length=50, blank=True, verbose_name="ORCID iD")

    @property
    def name(self): return self.get_tr('name')

    @property
    def position(self): return self.get_tr('position')

    @property
    def bio(self): return self.get_tr('bio')

    def __str__(self): return self.name_ru

    def get_absolute_url(self): return reverse('team_member_detail', kwargs={'slug': self.slug})

    class Meta: verbose_name = "Сотрудник"; verbose_name_plural = "Сотрудники"


class SocialLink(models.Model):
    member = models.ForeignKey(TeamMember, related_name='social_links', on_delete=models.CASCADE)
    icon_class = models.CharField(max_length=50, verbose_name="CSS класс иконки")
    url = models.URLField(verbose_name="URL-адрес ссылки")

    def __str__(self): return f"{self.member.name_ru} - {self.url}"

    class Meta: verbose_name = "Ссылка на соцсеть"; verbose_name_plural = "Ссылки на соцсети"


class ProjectFeature(TranslatableModel):
    project = models.ForeignKey('Project', related_name='features', on_delete=models.CASCADE, verbose_name="Проект")
    icon_class = models.CharField(max_length=100, verbose_name="CSS класс иконки")

    text_ru = models.CharField(max_length=200, verbose_name="Текст особенности (RU)")
    text_kk = models.CharField(max_length=200, verbose_name="Текст особенности (KK)", blank=True)
    text_en = models.CharField(max_length=200, verbose_name="Текст особенности (EN)", blank=True)
    order = models.PositiveIntegerField(default=0)

    @property
    def text(self): return self.get_tr('text')

    def __str__(self): return f"{self.project.title_ru} - {self.text_ru}"

    class Meta: verbose_name = "Особенность проекта"; verbose_name_plural = "Особенности проекта"; ordering = ['order']


class ProjectTechStack(models.Model):
    project = models.ForeignKey('Project', related_name='tech_stack', on_delete=models.CASCADE)
    icon_class = models.CharField(max_length=100, verbose_name="CSS класс иконки")
    text = models.CharField(max_length=100, verbose_name="Название технологии")  # Технологии обычно не переводят
    order = models.PositiveIntegerField(default=0)

    def __str__(self): return f"{self.project.title_ru} - {self.text}"

    class Meta: verbose_name = "Технология стека"; verbose_name_plural = "Технологический стек"; ordering = ['order']


class Project(TranslatableModel):
    CATEGORY_CHOICES = [('research', 'Научные проекты'), ('development', 'Разработка'),
                        ('commercial', 'Коммерциализация')]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='research')

    title_ru = models.CharField(max_length=100, verbose_name="Название (RU)")
    title_kk = models.CharField(max_length=100, verbose_name="Название (KK)", blank=True)
    title_en = models.CharField(max_length=100, verbose_name="Название (EN)", blank=True)

    slug = models.SlugField(max_length=100, unique=True)

    tagline_ru = models.CharField(max_length=200, verbose_name="Слоган (RU)")
    tagline_kk = models.CharField(max_length=200, verbose_name="Слоган (KK)", blank=True)
    tagline_en = models.CharField(max_length=200, verbose_name="Слоган (EN)", blank=True)

    status_tag_1_ru = models.CharField(max_length=50, blank=True, verbose_name="Статус 1 (RU)")
    status_tag_1_kk = models.CharField(max_length=50, blank=True, verbose_name="Статус 1 (KK)")
    status_tag_1_en = models.CharField(max_length=50, blank=True, verbose_name="Статус 1 (EN)")

    status_tag_2_ru = models.CharField(max_length=50, blank=True, verbose_name="Статус 2 (RU)")
    status_tag_2_kk = models.CharField(max_length=50, blank=True, verbose_name="Статус 2 (KK)")
    status_tag_2_en = models.CharField(max_length=50, blank=True, verbose_name="Статус 2 (EN)")

    full_description_ru = RichTextUploadingField(verbose_name="Описание (RU)")
    full_description_kk = RichTextUploadingField(verbose_name="Описание (KK)", blank=True)
    full_description_en = RichTextUploadingField(verbose_name="Описание (EN)", blank=True)

    external_link = models.URLField(blank=True, null=True)
    team = models.ManyToManyField('TeamMember', related_name='projects', verbose_name="Команда")

    task_description_ru = RichTextUploadingField(verbose_name="Задача (RU)", blank=True)
    task_description_kk = RichTextUploadingField(verbose_name="Задача (KK)", blank=True)
    task_description_en = RichTextUploadingField(verbose_name="Задача (EN)", blank=True)

    task_subtitle_ru = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок задачи (RU)")
    task_subtitle_kk = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок задачи (KK)")
    task_subtitle_en = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок задачи (EN)")

    result_description_ru = RichTextUploadingField(verbose_name="Результаты (RU)", blank=True)
    result_description_kk = RichTextUploadingField(verbose_name="Результаты (KK)", blank=True)
    result_description_en = RichTextUploadingField(verbose_name="Результаты (EN)", blank=True)

    detailed_info_ru = RichTextUploadingField(verbose_name="Доп. инфо (RU)", blank=True)
    detailed_info_kk = RichTextUploadingField(verbose_name="Доп. инфо (KK)", blank=True)
    detailed_info_en = RichTextUploadingField(verbose_name="Доп. инфо (EN)", blank=True)

    keywords = models.CharField(max_length=200, blank=True)

    @property
    def title(self): return self.get_tr('title')

    @property
    def tagline(self): return self.get_tr('tagline')

    @property
    def status_tag_1(self): return self.get_tr('status_tag_1')

    @property
    def status_tag_2(self): return self.get_tr('status_tag_2')

    @property
    def full_description(self): return self.get_tr('full_description')

    @property
    def task_description(self): return self.get_tr('task_description')

    @property
    def task_subtitle(self): return self.get_tr('task_subtitle')

    @property
    def result_description(self): return self.get_tr('result_description')

    @property
    def detailed_info(self): return self.get_tr('detailed_info')

    def __str__(self): return self.title_ru

    def get_absolute_url(self): return reverse('project_detail', kwargs={'slug': self.slug})

    class Meta: verbose_name = "Проект"; verbose_name_plural = "Проекты"


class ProjectResultImage(TranslatableModel):
    project = models.ForeignKey(Project, related_name='result_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='project_results/')
    caption_ru = models.CharField(max_length=255, blank=True)
    caption_kk = models.CharField(max_length=255, blank=True)
    caption_en = models.CharField(max_length=255, blank=True)

    @property
    def caption(self): return self.get_tr('caption')

    def __str__(self): return f"Img: {self.project.title_ru}"

    class Meta: verbose_name = "Изображение результата"; verbose_name_plural = "Изображения результатов"


class News(TranslatableModel):

    CATEGORY_CHOICES = [
        ('events', 'События'),
        ('research', 'Исследования'),
        ('partnership', 'Партнерство'),
        ('other', 'Другое'),
    ]

    title_ru = models.CharField(max_length=200, verbose_name="Заголовок (RU)")
    title_kk = models.CharField(max_length=200, verbose_name="Заголовок (KK)", blank=True)
    title_en = models.CharField(max_length=200, verbose_name="Заголовок (EN)", blank=True)

    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='news_images/')

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='events')

    content_ru = RichTextUploadingField(verbose_name="Содержание (RU)")
    content_kk = RichTextUploadingField(verbose_name="Содержание (KK)", blank=True)
    content_en = RichTextUploadingField(verbose_name="Содержание (EN)", blank=True)

    published_date = models.DateField()
    project = models.ForeignKey(Project, related_name='news', on_delete=models.SET_NULL, null=True, blank=True)
    author_name = models.CharField(max_length=100, blank=True, null=True)
    keywords = models.CharField(max_length=200, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def title(self): return self.get_tr('title')

    @property
    def content(self): return self.get_tr('content')

    def __str__(self): return self.title_ru

    def get_absolute_url(self): return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta: verbose_name = "Новость"; verbose_name_plural = "Новости"; ordering = ['-published_date']


class Service(TranslatableModel):
    title_ru = models.CharField(max_length=100)
    title_kk = models.CharField(max_length=100, blank=True)
    title_en = models.CharField(max_length=100, blank=True)

    description_ru = models.TextField()
    description_kk = models.TextField(blank=True)
    description_en = models.TextField(blank=True)

    icon_class = models.CharField(max_length=100, blank=True)
    order = models.PositiveIntegerField(default=0)

    @property
    def title(self): return self.get_tr('title')

    @property
    def description(self): return self.get_tr('description')

    class Meta: verbose_name = "Услуга"; verbose_name_plural = "Услуги"; ordering = ['order']

    def __str__(self): return self.title_ru