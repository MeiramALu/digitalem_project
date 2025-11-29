from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


# --- Вспомогательные функции ---

class Publication(models.Model):
    member = models.ForeignKey(
        'TeamMember',
        related_name='publications',
        on_delete=models.CASCADE,
        verbose_name="Сотрудник"
    )
    # Трехъязычные заголовки
    title_ru = models.CharField(max_length=255, verbose_name="Название статьи (RU)")
    title_kk = models.CharField(max_length=255, verbose_name="Название статьи (KK)", blank=True)
    title_en = models.CharField(max_length=255, verbose_name="Название статьи (EN)", blank=True)

    source = models.CharField(max_length=200, verbose_name="Журнал или источник")
    publication_date = models.DateField(verbose_name="Дата публикации")

    # Трехъязычное описание
    description_ru = RichTextUploadingField(verbose_name="Краткое описание (RU)", blank=True)
    description_kk = RichTextUploadingField(verbose_name="Краткое описание (KK)", blank=True)
    description_en = RichTextUploadingField(verbose_name="Краткое описание (EN)", blank=True)

    url = models.URLField(verbose_name="Ссылка на публикацию", blank=True)

    project = models.ForeignKey(
        'Project',
        related_name='publications',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Связанный проект"
    )

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-publication_date', 'title_ru']


class TeamMember(models.Model):
    name_ru = models.CharField(max_length=100, verbose_name="Имя и Фамилия (RU)")
    name_kk = models.CharField(max_length=100, verbose_name="Имя и Фамилия (KK)", blank=True)
    name_en = models.CharField(max_length=100, verbose_name="Имя и Фамилия (EN)", blank=True)

    is_visible = models.BooleanField(default=True, verbose_name="Отображать на сайте?")

    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-адрес (слаг)")

    position_ru = models.CharField(max_length=100, verbose_name="Должность (RU)", blank=True)
    position_kk = models.CharField(max_length=100, verbose_name="Должность (KK)", blank=True)
    position_en = models.CharField(max_length=100, verbose_name="Должность (EN)", blank=True)

    bio_ru = RichTextUploadingField(verbose_name="Биография (RU)", blank=True)
    bio_kk = RichTextUploadingField(verbose_name="Биография (KK)", blank=True)
    bio_en = RichTextUploadingField(verbose_name="Биография (EN)", blank=True)

    photo = models.ImageField(upload_to='team_photos/', verbose_name="Фотография")
    scopus_id = models.CharField(max_length=50, blank=True, verbose_name="Scopus Author ID")
    orcid_id = models.CharField(max_length=50, blank=True, verbose_name="ORCID iD")

    def __str__(self):
        return self.name_ru

    def get_absolute_url(self):
        return reverse('team_member_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"


class SocialLink(models.Model):
    member = models.ForeignKey(TeamMember, related_name='social_links', on_delete=models.CASCADE)
    icon_class = models.CharField(max_length=50, verbose_name="CSS класс иконки",
                                  help_text="Например: 'fab fa-linkedin' или 'bi bi-telegram'")
    url = models.URLField(verbose_name="URL-адрес ссылки")

    def __str__(self):
        return f"{self.member.name_ru} - {self.url}"

    class Meta:
        verbose_name = "Ссылка на соцсеть"
        verbose_name_plural = "Ссылки на соцсети"



class ProjectFeature(models.Model):
    project = models.ForeignKey('Project', related_name='features', on_delete=models.CASCADE, verbose_name="Проект")
    icon_class = models.CharField(max_length=100, verbose_name="CSS класс иконки",
                                  help_text="Например: 'fas fa-chart-line'")

    text_ru = models.CharField(max_length=200, verbose_name="Текст особенности (RU)")
    text_kk = models.CharField(max_length=200, verbose_name="Текст особенности (KK)", blank=True)
    text_en = models.CharField(max_length=200, verbose_name="Текст особенности (EN)", blank=True)

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self): return f"{self.project.title_ru} - {self.text_ru}"

    class Meta:
        verbose_name = "Особенность проекта"
        verbose_name_plural = "Особенности проекта"
        ordering = ['order']


class ProjectTechStack(models.Model):
    project = models.ForeignKey('Project', related_name='tech_stack', on_delete=models.CASCADE, verbose_name="Проект")
    icon_class = models.CharField(max_length=100, verbose_name="CSS класс иконки",
                                  help_text="Например: 'fab fa-python'")

    text = models.CharField(max_length=100, verbose_name="Название технологии")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self): return f"{self.project.title_ru} - {self.text}"

    class Meta:
        verbose_name = "Технология стека"
        verbose_name_plural = "Технологический стек"
        ordering = ['order']


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('research', 'Научные проекты и разработки'),
        ('development', 'Коммерциализационные проекты и разработки'),
        ('commercial', 'Коммерциализация'),
    ]
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default='research',
        verbose_name="Категория"
    )

    title_ru = models.CharField(max_length=100, verbose_name="Название проекта (RU)")
    title_kk = models.CharField(max_length=100, verbose_name="Название проекта (KK)", blank=True)
    title_en = models.CharField(max_length=100, verbose_name="Название проекта (EN)", blank=True)

    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-адрес (слаг)")

    tagline_ru = models.CharField(max_length=200, verbose_name="Слоган (RU)")
    tagline_kk = models.CharField(max_length=200, verbose_name="Слоган (KK)", blank=True)
    tagline_en = models.CharField(max_length=200, verbose_name="Слоган (EN)", blank=True)

    status_tag_1_ru = models.CharField(max_length=50, blank=True, verbose_name="Статус 1 (RU)")
    status_tag_1_kk = models.CharField(max_length=50, blank=True, verbose_name="Статус 1 (KK)")
    status_tag_1_en = models.CharField(max_length=50, blank=True, verbose_name="Статус 1 (EN)")

    status_tag_2_ru = models.CharField(max_length=50, blank=True, verbose_name="Статус 2 (RU)")
    status_tag_2_kk = models.CharField(max_length=50, blank=True, verbose_name="Статус 2 (KK)")
    status_tag_2_en = models.CharField(max_length=50, blank=True, verbose_name="Статус 2 (EN)")

    full_description_ru = RichTextUploadingField(verbose_name="Основное описание (RU)")
    full_description_kk = RichTextUploadingField(verbose_name="Основное описание (KK)", blank=True)
    full_description_en = RichTextUploadingField(verbose_name="Основное описание (EN)", blank=True)

    external_link = models.URLField(blank=True, null=True, verbose_name="Внешняя ссылка на проект")
    team = models.ManyToManyField('TeamMember', related_name='projects', verbose_name="Команда проекта")

    task_description_ru = RichTextUploadingField(verbose_name="Задача проекта (RU)", blank=True)
    task_description_kk = RichTextUploadingField(verbose_name="Задача проекта (KK)", blank=True)
    task_description_en = RichTextUploadingField(verbose_name="Задача проекта (EN)", blank=True)

    task_subtitle_ru = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок задачи (RU)")
    task_subtitle_kk = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок задачи (KK)")
    task_subtitle_en = models.CharField(max_length=200, blank=True, verbose_name="Подзаголовок задачи (EN)")

    result_description_ru = RichTextUploadingField(verbose_name="Результаты проекта (RU)", blank=True)
    result_description_kk = RichTextUploadingField(verbose_name="Результаты проекта (KK)", blank=True)
    result_description_en = RichTextUploadingField(verbose_name="Результаты проекта (EN)", blank=True)

    detailed_info_ru = RichTextUploadingField(verbose_name="Доп. информация (RU)", blank=True)
    detailed_info_kk = RichTextUploadingField(verbose_name="Доп. информация (KK)", blank=True)
    detailed_info_en = RichTextUploadingField(verbose_name="Доп. информация (EN)", blank=True)

    keywords = models.CharField(max_length=200, blank=True, verbose_name="Ключевые слова (SEO)")

    def __str__(self):
        return self.title_ru

    def get_absolute_url(self):
        return reverse('project_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Проект"
        verbose_name_plural = "Проекты"


class ProjectResultImage(models.Model):
    project = models.ForeignKey(
        Project,
        related_name='result_images',
        on_delete=models.CASCADE,
        verbose_name="Проект"
    )
    image = models.ImageField(upload_to='project_results/', verbose_name="Изображение")

    caption_ru = models.CharField(max_length=255, blank=True, verbose_name="Подпись (RU)")
    caption_kk = models.CharField(max_length=255, blank=True, verbose_name="Подпись (KK)")
    caption_en = models.CharField(max_length=255, blank=True, verbose_name="Подпись (EN)")

    def __str__(self):
        return f"Изображение для {self.project.title_ru}"

    class Meta:
        verbose_name = "Изображение результата"
        verbose_name_plural = "Изображения результатов"


class News(models.Model):
    title_ru = models.CharField(max_length=200, verbose_name="Заголовок (RU)")
    title_kk = models.CharField(max_length=200, verbose_name="Заголовок (KK)", blank=True)
    title_en = models.CharField(max_length=200, verbose_name="Заголовок (EN)", blank=True)

    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-адрес (слаг)")
    image = models.ImageField(upload_to='news_images/', verbose_name="Изображение")
    category = models.CharField(max_length=50, verbose_name="Категория")

    content_ru = RichTextUploadingField(verbose_name="Содержание (RU)")
    content_kk = RichTextUploadingField(verbose_name="Содержание (KK)", blank=True)
    content_en = RichTextUploadingField(verbose_name="Содержание (EN)", blank=True)

    published_date = models.DateField(verbose_name="Дата публикации")
    project = models.ForeignKey(
        Project,
        related_name='news',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Связанный проект"
    )
    author_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя автора")
    keywords = models.CharField(max_length=200, blank=True, verbose_name="Ключевые слова (через запятую)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return self.title_ru

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']


class Service(models.Model):
    title_ru = models.CharField(max_length=100, verbose_name="Название услуги (RU)")
    title_kk = models.CharField(max_length=100, verbose_name="Название услуги (KK)", blank=True)
    title_en = models.CharField(max_length=100, verbose_name="Название услуги (EN)", blank=True)

    description_ru = models.TextField(verbose_name="Краткое описание (RU)")
    description_kk = models.TextField(verbose_name="Краткое описание (KK)", blank=True)
    description_en = models.TextField(verbose_name="Краткое описание (EN)", blank=True)

    icon_class = models.CharField(max_length=100, verbose_name="CSS класс иконки", help_text="Например: 'fas fa-cogs'",
                                  blank=True)

    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order']

    def __str__(self):
        return self.title_ru