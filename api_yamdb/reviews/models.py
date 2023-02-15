from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from users.models import User


class Category(models.Model):
    """Модель для категорий произведений."""

    name = models.CharField(max_length=255, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Класс для жанров произведений."""
    name = models.CharField(max_length=255, verbose_name='Название жанра')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title (models.Model):
    """Класс для произведений, к которым пишут отзывы и оценивают."""
    name = models.CharField(
        max_length=255, verbose_name='Название произведения')
    year = models.IntegerField(
        validators=[MaxValueValidator(timezone.now().year)],
        verbose_name='Год выпуска',
        db_index=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='genre',
        verbose_name='Жанр'
    )
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='category',
        verbose_name='Категория'
    )

    description = models.TextField(
        max_length=200,
        null=True,
    )

    class Meta:
        verbose_name = "Произведение"
        verbose_name_plural = "Произведения"
        ordering = ('-id',)

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзывов плюс рейтинг"""
    author = models.ForeignKey(
        User,
        related_name='reviews',
        on_delete=models.CASCADE,
        verbose_name='Автор отзыва',
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Оцениваемое произведение',
    )
    text = models.TextField('Текст отзыва')
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True
    )
    score = models.IntegerField(
        blank=True,
        validators=[MinValueValidator(1, 'Допустимы значения от 1 до 10'),
                    MaxValueValidator(10, 'Допустимы значения от 1 до 10')
                    ]
    )

    class Meta:
        unique_together = ('title', 'author',)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'


class Comments(models.Model):
    """Модель комментариев"""
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        related_name='comments',
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        related_name='comments',
        on_delete=models.CASCADE
    )
    text = models.TextField('Текст комментария')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Жанр')

    title = models.ForeignKey(
        Title, null=True,
        on_delete=models.SET_NULL,
        verbose_name='Произведение')

    class Meta:
        verbose_name = 'Жанр произведения'
        verbose_name_plural = 'Жанры произведения'

    def __str__(self):
        return f'{self.title} {self.genre}'
