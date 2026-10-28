
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


NIGERIAN_STATES = [
    ("Abia", "Abia"),
    ("Adamawa", "Adamawa"),
    ("Akwa Ibom", "Akwa Ibom"),
    ("Anambra", "Anambra"),
    ("Bauchi", "Bauchi"),
    ("Bayelsa", "Bayelsa"),
    ("Benue", "Benue"),
    ("Borno", "Borno"),
    ("Cross River", "Cross River"),
    ("Delta", "Delta"),
    ("Ebonyi", "Ebonyi"),
    ("Edo", "Edo"),
    ("Ekiti", "Ekiti"),
    ("Enugu", "Enugu"),
    ("FCT", "Federal Capital Territory"),
    ("Gombe", "Gombe"),
    ("Imo", "Imo"),
    ("Jigawa", "Jigawa"),
    ("Kaduna", "Kaduna"),
    ("Kano", "Kano"),
    ("Katsina", "Katsina"),
    ("Kebbi", "Kebbi"),
    ("Kogi", "Kogi"),
    ("Kwara", "Kwara"),
    ("Lagos", "Lagos"),
    ("Nasarawa", "Nasarawa"),
    ("Niger", "Niger"),
    ("Ogun", "Ogun"),
    ("Ondo", "Ondo"),
    ("Osun", "Osun"),
    ("Oyo", "Oyo"),
    ("Plateau", "Plateau"),
    ("Rivers", "Rivers"),
    ("Sokoto", "Sokoto"),
    ("Taraba", "Taraba"),
    ("Yobe", "Yobe"),
    ("Zamfara", "Zamfara"),
]


class MusicianProfile(models.Model):
    class Category(models.TextChoices):
        SINGER = "singer", "Singer"
        INSTRUMENTALIST = "instrumentalist", "Instrumentalist"

    class VocalPart(models.TextChoices):
        SOPRANO = "soprano", "Soprano"
        MEZZO_SOPRANO = "mezzo_soprano", "Mezzo-soprano"
        ALTO = "alto", "Alto"
        TENOR = "tenor", "Tenor"
        BARITONE = "baritone", "Baritone"
        BASS = "bass", "Bass"
        OTHER = "other", "Other"

    class PerformanceType(models.TextChoices):
        SOLO = "solo", "Solo performer"
        BAND = "band", "Band / ensemble"

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="musician_profile",
    )
    display_name = models.CharField(max_length=100)
    bio = models.CharField(max_length=200, blank=True)
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )
    state = models.CharField(
        max_length=20,
        choices=NIGERIAN_STATES,
    )
    city = models.CharField(max_length=100)
    profile_photo = models.ImageField(
        upload_to="musicians/profiles/",
        blank=True,
        null=True,
    )
    vocal_part = models.CharField(
        max_length=20,
        choices=VocalPart.choices,
        blank=True,
    )
    performance_type = models.CharField(
        max_length=10,
        choices=PerformanceType.choices,
        blank=True,
    )
    band_size = models.PositiveSmallIntegerField(
        blank=True,
        null=True,
        validators=[
            MinValueValidator(2),
            MaxValueValidator(100),
        ],
    )
    is_verified = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_name"]

    def __str__(self):
        return self.display_name


class MusicianService(models.Model):
    class Instrument(models.TextChoices):
        VIOLIN = "violin", "Violin"
        PIANO = "piano", "Piano / Keyboard"
        GUITAR = "guitar", "Guitar"
        DRUMS = "drums", "Drums"
        SAXOPHONE = "saxophone", "Saxophone"
        BASS_GUITAR = "bass_guitar", "Bass guitar"
        TRUMPET = "trumpet", "Trumpet"
        FLUTE = "flute", "Flute"
        PERCUSSION = "percussion", "Percussion"
        OTHER = "other", "Other instrument"
        VOCALS = "vocals", "Singing / Vocals"

    musician = models.ForeignKey(
        MusicianProfile,
        on_delete=models.CASCADE,
        related_name="services",
    )
    instrument = models.CharField(
        max_length=20,
        choices=Instrument.choices,
    )
    service_name = models.CharField(max_length=120)
    description = models.CharField(max_length=200, blank=True)
    starting_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["starting_price", "service_name"]

    def __str__(self):
        return f"{self.musician.display_name} — {self.service_name}"
