from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from guardian.shortcuts import assign_perm

# Kullanıcı modeli
User = get_user_model()

# Hasta Modeli
class Patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    phone = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    medical_history = models.TextField(null=True, blank=True)
    therapist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='patients',
        default=1  # Varsayılan olarak ID'si 1 olan kullanıcı
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Yeni kayıt mı kontrol et
        super().save(*args, **kwargs)
        if is_new:  # Yeni kayıtsa izinleri ata
            assign_perm('patients.view_patient', self.therapist, self)
            assign_perm('patients.change_patient', self.therapist, self)


# Randevu Modeli
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    therapist = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    date_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='scheduled'
    )
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Appointment with {self.patient} on {self.date_time}"
