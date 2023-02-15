from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models

ROLES = [
    ('user', 'Аутентифицированный пользователь'),
    ('moderator', 'Модератор'), ('admin', 'Администратор'),
    ('superuser', 'Суперюзер Django')
]


class User(AbstractUser):
    """Кастомная модель пользователя."""

    username = models.CharField(max_length=150, unique=True,
                                validators=[UnicodeUsernameValidator],)
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        choices=ROLES, max_length=35, default='user'
    )
    confirmation_code = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def save(self, *args, **kwargs):
        """При сохранении в поле роль ставит admin если это супер юзер"""
        if self.is_superuser:
            self.role = 'admin'
        super(User, self).save()

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == str(ROLES[0][0])

    @property
    def is_moderator(self):
        return self.role == str(ROLES[1][0])

    @property
    def is_admin(self):
        return self.role == str(ROLES[2][0])

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'role', 'confirmation_code']
