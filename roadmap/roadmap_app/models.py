from django.db import models


class Organization(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название организации")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    city = models.CharField(max_length=100, verbose_name="Город")
    website = models.URLField(blank=True, null=True, verbose_name="Сайт")
    logo = models.ImageField(upload_to="logos/", blank=True, null=True, verbose_name="Логотип")

    def __str__(self):
        return self.name


class EducationInstitution(models.Model):
    TYPE_CHOICES = [
        ("vuz", "ВУЗ"),
        ("suz", "СУЗ"),
    ]

    name = models.CharField(max_length=255, verbose_name="Название образовательной организации")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, verbose_name="Тип")
    city = models.CharField(max_length=100, verbose_name="Город")
    website = models.URLField(blank=True, null=True, verbose_name="Сайт")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})" #type:ignore


class SupportMeasure(models.Model):
    TYPE_CHOICES = [
        ("internship", "Стажировка"),
        ("start", "Начальная позиция"),
        ("career", "Карьера"),
    ]

    description = models.TextField(blank=True, null=True, verbose_name="Описание меры")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Тип меры поддержки")

    def __str__(self):
        type_display = self.get_type_display() if self.type else "" # type:ignore
        text = self.description.strip() if self.description else "" # type:ignore
        return f"{text[:80]}{'...' if len(text) > 80 else ''} ({type_display})"



class Specialty(models.Model):
    name = models.CharField(blank=True, null=True, max_length=255, verbose_name="Специальность / Направление подготовки")
    institution = models.ForeignKey(
        EducationInstitution, blank=True, null=True, on_delete=models.CASCADE, related_name="specialties", verbose_name="Учебное заведение"
    )
    organization = models.ForeignKey(
        Organization, blank=True, null=True, on_delete=models.CASCADE, related_name="specialties", verbose_name="Организация"
    )
    has_internship = models.BooleanField(default=False, verbose_name="Есть стажировка")
    intern_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="Стажерская позиция")

    # Связи с мерами поддержки. НЕ МЕНЯТЬ!!
    start_position = models.CharField(max_length=255, blank=True, null=True, verbose_name="Начальная позиция")
    next_positions = models.TextField(blank=True, null=True, verbose_name="Последующие позиции")
    intern_support = models.ManyToManyField(
        SupportMeasure,
        blank=True,
        related_name="intern_specialties",
        limit_choices_to={"type": "internship"},
        verbose_name="Меры поддержки (стажировка)"
    )
    start_support = models.ManyToManyField(
        SupportMeasure,
        blank=True,
        related_name="start_specialties",
        limit_choices_to={"type": "start"},
        verbose_name="Меры поддержки (начальная позиция)"
    )
    next_support = models.ManyToManyField(
        SupportMeasure,
        blank=True,
        related_name="career_specialties",
        limit_choices_to={"type": "career"},
        verbose_name="Меры поддержки (последующие позиции)"
    )
    def __str__(self):
        return f"{self.name} ({self.institution.name})"


class Roadmap(models.Model):
    school = models.CharField(max_length=255, verbose_name="Этап школы (доп. предметы)")
    education = models.ForeignKey(
        EducationInstitution, on_delete=models.CASCADE, related_name="roadmaps", verbose_name="Образование"
    )
    specialty = models.ForeignKey(
        Specialty, on_delete=models.CASCADE, related_name="roadmaps", verbose_name="Специальность"
    )
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name="roadmaps", verbose_name="Организация"
    )
    career_path = models.TextField(verbose_name="Описание карьерного пути")

    def __str__(self):
        return f"Путь: {self.education.name} → {self.organization.name}"


class UserPath(models.Model):
    CLASS_CHOICES = [
        ("9", "После 9 класса"),
        ("11", "После 11 класса"),
    ]

    EDUCATION_TYPE_CHOICES = [
        ("vuz", "ВУЗ"),
        ("suz", "СУЗ"),
    ]

    entry_after = models.CharField(max_length=2, choices=CLASS_CHOICES, verbose_name="Поступление после класса")
    education_type = models.CharField(max_length=10, choices=EDUCATION_TYPE_CHOICES, verbose_name="Тип образования")
    specialty = models.ForeignKey(
        Specialty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Выбранная специальность"
    )
    needs_internship = models.BooleanField(default=False, verbose_name="Нужна ли стажировка")
    career_goal = models.CharField(max_length=255, blank=True, null=True, verbose_name="Желаемая позиция")
    recommended_institution = models.ForeignKey(
        EducationInstitution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recommended_paths",
        verbose_name="Рекомендуемое учебное заведение"
    )
    recommended_organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="recommended_paths",
        verbose_name="Рекомендуемая организация"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Путь пользователя ({self.get_entry_after_display()}" #type:ignore
                f" → {self.get_education_type_display()})") #type:ignore
