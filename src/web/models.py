"""The company is the authenticated principal (AD-6) and owns its data (AD-7, AD-8)."""

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models

from forecasting import settings as defaults


class CompanyManager(BaseUserManager):
    def create_user(self, customer_number, password=None, **extra_fields):
        """Create a company; Django's default PBKDF2 hasher hashes the password."""
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


class Product(models.Model):
    """A product with its stock on hand, read-only in the app (FR-3, FR-4)."""

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="bedrift",
    )
    product_number = models.CharField("varenummer", max_length=5)
    name = models.CharField("navn", max_length=200)
    stock_on_hand = models.PositiveIntegerField("lager")

    class Meta:
        verbose_name = "produkt"
        verbose_name_plural = "produkter"
        constraints = (
            models.UniqueConstraint(
                fields=["company", "product_number"], name="unique_product_number"
            ),
        )

    def __str__(self):
        return f"{self.product_number} {self.name}"


class SalesWeek(models.Model):
    """One week of a product's history, identified by its position from 1 to N (AD-8).

    The company's latest data week is never stored: it is the latest ISO year and
    week among its sales weeks.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="sales_weeks",
        verbose_name="produkt",
    )
    position = models.PositiveIntegerField("posisjon")
    iso_year = models.PositiveSmallIntegerField("ISO-år")
    iso_week = models.PositiveSmallIntegerField("ISO-uke")
    units_sold = models.PositiveIntegerField("solgte enheter")
    stockout = models.BooleanField("utsolgt")

    class Meta:
        verbose_name = "salgsuke"
        verbose_name_plural = "salgsuker"
        constraints = (
            models.UniqueConstraint(
                fields=["product", "position"], name="unique_sales_week_position"
            ),
        )

    def __str__(self):
        return f"{self.product} {self.iso_year}-W{self.iso_week:02d}"


class CompanySettings(models.Model):
    """The company-wide settings of FR-20. The defaults come from the core (AD-9)."""

    METHOD_CHOICES = (
        (defaults.MOVING_AVERAGE, "Glidende gjennomsnitt"),
        (defaults.EXPONENTIAL_SMOOTHING, "Eksponentiell glatting"),
    )

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name="company_settings",
        verbose_name="bedrift",
    )
    method = models.CharField(
        "prognosemetode",
        max_length=max(len(method) for method in defaults.METHODS),
        choices=METHOD_CHOICES,
        default=defaults.DEFAULT_METHOD,
    )
    window = models.PositiveSmallIntegerField("vindu", default=defaults.WINDOW.default)
    smoothing_factor = models.DecimalField(
        "glattingsfaktor",
        max_digits=2,
        decimal_places=1,
        default=defaults.SMOOTHING_FACTOR.default,
    )
    scenario_percentage = models.PositiveSmallIntegerField(
        "scenarioprosent", default=defaults.SCENARIO_PERCENTAGE.default
    )
    safety_margin = models.PositiveSmallIntegerField(
        "sikkerhetsmargin", default=defaults.SAFETY_MARGIN.default
    )
    unusual_weeks_included = models.BooleanField(
        "uvanlige uker med", default=defaults.DEFAULT_UNUSUAL_WEEKS_INCLUDED
    )
    seasonal_adjustment = models.BooleanField(
        "sesongjustering", default=defaults.DEFAULT_SEASONAL_ADJUSTMENT
    )

    class Meta:
        verbose_name = "innstillinger"
        verbose_name_plural = "innstillinger"

    def __str__(self):
        return f"Innstillinger for {self.company}"
