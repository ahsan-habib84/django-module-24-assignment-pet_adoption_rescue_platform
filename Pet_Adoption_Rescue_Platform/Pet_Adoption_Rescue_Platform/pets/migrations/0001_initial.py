from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency("auth.User"),
    ]
    operations = [
        migrations.CreateModel(
            name="Pet",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("animal_type", models.CharField(choices=[("Dog","Dog"),("Cat","Cat"),("Bird","Bird"),("Rabbit","Rabbit"),("Other","Other")], max_length=30)),
                ("breed", models.CharField(blank=True, max_length=100)),
                ("age", models.PositiveIntegerField(help_text="Age in years")),
                ("gender", models.CharField(choices=[("Male","Male"),("Female","Female")], max_length=10)),
                ("location", models.CharField(max_length=100)),
                ("description", models.TextField()),
                ("image", models.ImageField(blank=True, null=True, upload_to="pets/")),
                ("status", models.CharField(choices=[("Available","Available"),("Adopted","Adopted")], default="Available", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={"ordering":["-created_at"]},
        ),
        migrations.CreateModel(
            name="AdoptionRequest",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(max_length=30)),
                ("address", models.TextField()),
                ("reason", models.TextField()),
                ("previous_pet_experience", models.BooleanField(default=False)),
                ("message", models.TextField(blank=True)),
                ("status", models.CharField(choices=[("Pending","Pending"),("Approved","Approved"),("Rejected","Rejected")], default="Pending", max_length=20)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("pet", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="adoption_requests", to="pets.pet")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="adoption_requests", to="auth.user")),
            ],
            options={"ordering":["-created_at"]},
        ),
    ]
