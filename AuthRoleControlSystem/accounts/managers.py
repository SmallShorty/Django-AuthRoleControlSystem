from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name, middle_name=None):
        # создаём объект модели
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )

        # хешируем пароль
        user.set_password(password)

        # проверяем обязательные поля
        try:
            user.full_clean()
        except ValidationError as e:
            raise ValidationError(f"Ошибка создания пользователя: {e}")

        # сохраняем
        user.save(using=self._db)
        return user
