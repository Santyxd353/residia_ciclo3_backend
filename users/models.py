from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)

        # asegura username porque AbstractUser lo requiere único
        if not getattr(user, 'username', None):
            base = (email or '').split('@')[0] or 'user'
            candidate = base
            i = 1
            # evitar colisiones
            while self.model.objects.filter(username=candidate).exists():
                i += 1
                candidate = f"{base}{i}"
            user.username = candidate

        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()

        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # por compatibilidad si algo pasa 'username' en vez de 'email'
        if not email and 'username' in extra_fields:
            email = extra_fields.pop('username')

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'ADMIN')
        extra_fields.setdefault('status', 'ACTIVE')

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        SECURITY = 'SECURITY', 'Security'
        MAINTENANCE = 'MAINTENANCE', 'Maintenance'
        RESIDENT = 'RESIDENT', 'Resident'

    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', 'Active'
        INACTIVE = 'INACTIVE', 'Inactive'
        SUSPENDED = 'SUSPENDED', 'Suspended'

    # --- login por email ---
    email = models.EmailField(unique=True)

    # Campos adicionales
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.RESIDENT)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)

    national_id = models.CharField(max_length=20, unique=True, null=True, blank=True)  # CI
    phone = models.CharField(max_length=32, null=True, blank=True)
    photo_url = models.TextField(null=True, blank=True)

    # Autenticación por email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no pedimos username en createsuperuser

    objects = UserManager()

    def save(self, *args, **kwargs):
        # doble seguro: si por alguna razón llega sin username, lo generamos
        if not self.username:
            base = (self.email or '').split('@')[0] or 'user'
            candidate = base
            i = 1
            from django.contrib.auth import get_user_model
            UserModel = get_user_model()
            while UserModel.objects.filter(username=candidate).exclude(pk=self.pk).exists():
                i += 1
                candidate = f"{base}{i}"
            self.username = candidate
        super().save(*args, **kwargs)
