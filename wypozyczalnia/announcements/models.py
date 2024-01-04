from django.db import models
from django.conf import settings
from django.utils import timezone

GRADE = (
    ('1', '1'),
    ('2', '2'),
    ('3', '3'),
    ('4', '4'),
    ('5', '5'),
    ('6', '6'),
    ('7', '7'),
    ('8', '8'),
    ('9', '9'),
    ('10', '10'),
)

TYPE = (
    ('1', 'Gry'),
    ('2', 'Ksiązki'),
    ('3', 'Filmy'),
    ('4', 'Elektronika'),
    ('5', 'Sport'),
    ('6', 'Muzyka'),
)


class Announcement(models.Model):

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, verbose_name="Autor")
    create_date = models.DateTimeField(default=timezone.now, verbose_name="Data utworzenia")
    name = models.CharField(max_length=100, verbose_name="Nazwa produktu")
    type = models.CharField(choices=TYPE, max_length=2, default=None, verbose_name="Rodzaj")
    description = models.TextField(blank=True, verbose_name="Opis")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Cena")
    photo = models.ImageField(upload_to='announcement/', null=True, blank=True, verbose_name="Zdjęcie")
    available = models.BooleanField(default=True, verbose_name="Dostępność")

    def __str__(self):
        return self.name


class Rating(models.Model):
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='comments', verbose_name="Ogłoszenie")
    grade = models.CharField(choices=GRADE, max_length=2, verbose_name="Ocena")
    comment = models.TextField(max_length=250, verbose_name="Komentarz")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.CASCADE, verbose_name="Użytkownik")
    create_date = models.DateTimeField(default=timezone.now, verbose_name="Data utworzenia")

    def __str__(self):
        return ''


class Borrowing(models.Model):

    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='borrowings', verbose_name="Ogłoszenie")
    borrower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='borrowings', verbose_name="Wypożyczający")
    borrow_date = models.DateField(verbose_name="Data wypożyczenia")
    return_date = models.DateField(blank=True, null=True, verbose_name="Data zwrotu")

    def __str__(self):
        return self.announcement.name + ' - ' + str(self.borrower)

