from django.contrib import admin
from .models import Pet, AdoptionRequest

@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ("name", "animal_type", "breed", "gender", "location", "status", "created_at")
    list_filter = ("animal_type", "gender", "status", "location")
    search_fields = ("name", "breed", "location")

@admin.register(AdoptionRequest)
class AdoptionRequestAdmin(admin.ModelAdmin):
    list_display = ("user", "pet", "phone", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("user__username", "pet__name", "phone")
    list_select_related = ("user", "pet")

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.status == "Approved":
            obj.pet.status = "Adopted"
            obj.pet.save(update_fields=["status"])
