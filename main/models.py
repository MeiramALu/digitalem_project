from django.db import models
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField


class Publication(models.Model):
    member = models.ForeignKey(
        'TeamMember',
        related_name='publications',
        on_delete=models.CASCADE,
        verbose_name="Сотрудник"
    )
    title = models.CharField(max_length=255, verbose_name="Название статьи")
    source = models.CharField(max_length=200, verbose_name="Журнал или источник")
    publication_date = models.DateField(verbose_name="Дата публикации")
    # ИЗМЕНЕНО: TextField -> RichTextUploadingField
    description = RichTextUploadingField(verbose_name="Краткое описание", blank=True)
    url = models.URLField(verbose_name="Ссылка на публикацию", blank=True)

    project = models.ForeignKey(
        'Project',
        related_name='publications',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Связанный проект"
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Публикация"
        verbose_name_plural = "Публикации"
        ordering = ['-publication_date', 'title']


class TeamMember(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя и Фамилия")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-адрес (слаг)")
    position = models.CharField(max_length=100, verbose_name="Должность", blank=True)
    # ИЗМЕНЕНО: TextField -> RichTextUploadingField
    bio = RichTextUploadingField(verbose_name="Биография", blank=True)
    photo = models.ImageField(upload_to='team_photos/', verbose_name="Фотография")
    scopus_id = models.CharField(max_length=50, blank=True, verbose_name="Scopus Author ID")
    orcid_id = models.CharField(max_length=50, blank=True, verbose_name="ORCID iD")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('team_member_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Сотрудники"
        verbose_name_plural = "Сотрудники"


class SocialLink(models.Model):
    member = models.ForeignKey(TeamMember, related_name='social_links', on_delete=models.CASCADE)
    icon_class = models.CharField(max_length=50, verbose_name="CSS класс иконки (например, 'fab fa-linkedin')")
    url = models.URLField(verbose_name="URL-адрес ссылки")

    def __str__(self):
        return f"{self.member.name} - {self.url}"

    class Meta:
        verbose_name = "Ссылка на соцсеть"
        verbose_name_plural = "Ссылки на соцсети"


class Icon(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название иконки (для админки)")
    icon_class = models.CharField(max_length=50, verbose_name="CSS класс иконки (например, 'fas fa-chart-line')")

    def __str__(self): return self.title

    class Meta:
        verbose_name = "Иконка"
        verbose_name_plural = "Иконки"


class ProjectFeature(models.Model):
    project = models.ForeignKey('Project', related_name='features', on_delete=models.CASCADE, verbose_name="Проект")
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, verbose_name="Иконка")
    text = models.CharField(max_length=200, verbose_name="Текст особенности")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self): return f"{self.project.title} - {self.text}"

    class Meta:
        verbose_name = "Особенность проекта"
        verbose_name_plural = "Особенности проекта"
        ordering = ['order']


class ProjectTechStack(models.Model):
    project = models.ForeignKey('Project', related_name='tech_stack', on_delete=models.CASCADE, verbose_name="Проект")
    icon = models.ForeignKey(Icon, on_delete=models.CASCADE, verbose_name="Иконка")
    text = models.CharField(max_length=100, verbose_name="Название технологии")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self): return f"{self.project.title} - {self.text}"

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
    title = models.CharField(max_length=100, verbose_name="Название проекта")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="URL-адрес (слаг)")
    tagline = models.CharField(max_length=200, verbose_name="Слоган/Краткое описание")
    status_tag_1 = models.CharField(max_length=50, blank=True, verbose_name="Статус (тег 1)")
    status_tag_2 = models.CharField(max_length=50, blank=True, verbose_name="Статус (тег 2)")
    full_description = RichTextUploadingField(verbose_name="Основной абзац описания")
    external_link = models.URLField(blank=True, null=True, verbose_name="Внешняя ссылка на проект")
    team = models.ManyToManyField('TeamMember', related_name='projects', verbose_name="Команда проекта")
    task_description = RichTextUploadingField(verbose_name="Задача проекта", blank=True)
    task_subtitle = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Подзаголовок для задачи проекта"
    )
    result_description = RichTextUploadingField(verbose_name="Результаты проекта", blank=True)
    detailed_info = RichTextUploadingField(
        verbose_name="Дополнительная информация (для кнопки 'Подробнее')",
        blank=True
    )
    keywords = models.CharField(max_length=200, blank=True, verbose_name="Ключевые слова (через запятую)")
    def __str__(self):
        return self.title

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
    caption = models.CharField(max_length=255, blank=True, verbose_name="Подпись к изображению")

    def __str__(self):
        return f"Изображение для проекта {self.project.title}"

    class Meta:
        verbose_name = "Изображение результата"
        verbose_name_plural = "Изображения результатов"


class News(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="URL-адрес (слаг)")
    image = models.ImageField(upload_to='news_images/', verbose_name="Изображение")
    category = models.CharField(max_length=50, verbose_name="Категория",help_text="Например: Исследования, Партнерство")
    content = RichTextUploadingField(verbose_name="Содержание")
    published_date = models.DateField(verbose_name="Дата публикации")
    project = models.ForeignKey(
        Project,
        related_name='news',
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name="Связанный проект"
    )
    author_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Имя автора (текст)")
    keywords = models.CharField(max_length=200, blank=True, verbose_name="Ключевые слова (через запятую)")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Последнее обновление")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    class Meta:
        verbose_name = "Новость"
        verbose_name_plural = "Новости"
        ordering = ['-published_date']


class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название услуги")
    description = models.TextField(verbose_name="Краткое описание")
    icon = models.ForeignKey(
        Icon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Иконка"
    )
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок сортировки")

    class Meta:
        verbose_name = "Услуга"
        verbose_name_plural = "Услуги"
        ordering = ['order']

    def __str__(self):
        return self.title