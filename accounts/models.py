"""The company is the authenticated principal (AD-5)."""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class CompanyManager(BaseUserManager):
    def create_user(self, customer_number, password=None, **extra_fields):
        """Create a company. Django's default PBKDF2 hasher hashes the password."""
        if not customer_number:
            raise ValueError("Kundenummer mangler.")
        company = self.model(
            customer_number=self.model.normalize_username(customer_number),
            **extra_fields,
        )
        company.set_password(password)
        company.save(using=self._db)
        return company


class Company(AbstractBaseUser):
    """A business account that logs in with its customer number (FR-1)."""

    customer_number = models.CharField("kundenummer", max_length=20, unique=True)
    name = models.CharField("navn", max_length=200)

    objects = CompanyManager()

    USERNAME_FIELD = "customer_number"
    REQUIRED_FIELDS = ("name",)

    class Meta:
        verbose_name = "bedrift"
        verbose_name_plural = "bedrifter"

    def __str__(self):
        return self.name
