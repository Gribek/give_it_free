from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.utils.translation import ugettext_lazy as _


class UserManager(BaseUserManager):
    """New model manager for new User model"""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """New User model"""

    # remove username field inherited from AbstractUser model
    username = None
    email = models.EmailField(_('email address'), unique=True)

    # email field will be used as username filed before
    # with login, authentication, etc.
    USERNAME_FIELD = 'email'

    # remove email from REQUIRED_FIELDS,
    # USERNAME_FIELD is required automatically
    REQUIRED_FIELDS = []

    # assign new manager to User model
    objects = UserManager()


class TrustedInstitution(models.Model):
    """Represents a single trusted institution."""

    name = models.CharField(max_length=64, verbose_name='Nazwa instytucji')
    purpose = models.CharField(max_length=128, verbose_name='Cel i misja')
    needs = models.CharField(max_length=128, verbose_name='Potrzebne datki')
    localization = models.CharField(max_length=64, verbose_name='Lokalizacja')
    target_groups = models.ManyToManyField('TargetGroup',
                                           verbose_name='Grupy docelowe')

    def __str__(self):
        """Return a string representation of the model."""
        return self.name

    class Meta:
        verbose_name = 'Zaufaną instytucję'
        verbose_name_plural = 'Zaufane instytucje'


class TargetGroup(models.Model):
    name = models.CharField(max_length=32, verbose_name='Nazwa grupy')

    def __str__(self):
        """Return a string representation of the model."""
        return self.name

    class Meta:
        verbose_name = 'Grupę docelową'
        verbose_name_plural = 'Grupy docelowe'


class Gift(models.Model):
    """Represents a single gift."""

    gift_type = ArrayField(models.CharField(max_length=32))
    number_of_bags = models.SmallIntegerField()
    giver = models.ForeignKey(User, on_delete=models.CASCADE)
    trusted_institution = models.ForeignKey(TrustedInstitution,
                                            on_delete=models.CASCADE)
    creation_date = models.DateField(auto_now_add=True)
    transfer_date = models.DateField(null=True)
    is_transferred = models.BooleanField(default=False)
    pick_up_address = models.OneToOneField('PickUpAddress',
                                           on_delete=models.CASCADE)


class PickUpAddress(models.Model):
    """Represents a single pick up address."""

    street = models.CharField(max_length=64)
    city = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=8)
    phone_number = models.CharField(max_length=16)
    pick_up_date = models.DateField()
    pick_up_time = models.TimeField()
    comments = models.TextField(null=True)


class CharityCollection(models.Model):
    """Represents a single charity collection."""

    organizer = models.ForeignKey(User, on_delete=models.CASCADE)
    purpose = models.CharField(max_length=256, verbose_name='Cel zbiórki')
    items_needed = models.CharField(max_length=256,
                                    verbose_name='Co jest potrzebne')
    address = models.CharField(max_length=256, verbose_name='Pełen adres')
    creation_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(verbose_name='Termin końcowy zbiórki')
    is_authorized = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Zbiórka charytatywna'
        verbose_name_plural = 'Zbiórki charytatywne'
