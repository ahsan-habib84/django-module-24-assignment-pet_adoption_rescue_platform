from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

class Pet(models.Model):
    ANIMAL_TYPES = [
        ("Dog", "Dog"), ("Cat", "Cat"), ("Bird", "Bird"),
        ("Rabbit", "Rabbit"), ("Other", "Other"),
    ]
    GENDERS = [("Male", "Male"), ("Female", "Female")]
    STATUSES = [("Available", "Available"), ("Adopted", "Adopted")]

    name = models.CharField(max_length=100)
    animal_type = models.CharField(max_length=30, choices=ANIMAL_TYPES)
    breed = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField(help_text="Age in years")
    gender = models.CharField(max_length=10, choices=GENDERS)
    location = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to="pets/", blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUSES, default="Available")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class AdoptionRequest(models.Model):
    STATUSES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="adoption_requests")
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="adoption_requests")
    phone = models.CharField(max_length=30)
    address = models.TextField()
    reason = models.TextField()
    previous_pet_experience = models.BooleanField(default=False)
    message = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUSES, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def clean(self):
        if self.pet.status == "Adopted" and self.status == "Pending":
            raise ValidationError("This pet has already been adopted.")
        duplicate = AdoptionRequest.objects.filter(
            user=self.user, pet=self.pet, status__in=["Pending", "Approved"]
        ).exclude(pk=self.pk)
        if duplicate.exists() and self.status == "Pending":
            raise ValidationError("You already have an active request for this pet.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
