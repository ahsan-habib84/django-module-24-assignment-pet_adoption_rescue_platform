from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from .forms import AdoptionRequestForm
from .models import AdoptionRequest, Pet

def home(request):
    pets = Pet.objects.filter(status="Available")[:6]
    return render(request, "pets/home.html", {"pets": pets})

def pet_list(request):
    pets = Pet.objects.all()
    search = request.GET.get("search", "").strip()
    animal_type = request.GET.get("animal_type", "")
    breed = request.GET.get("breed", "").strip()
    gender = request.GET.get("gender", "")
    location = request.GET.get("location", "").strip()
    status = request.GET.get("status", "")

    if search:
        pets = pets.filter(name__icontains=search)
    if animal_type:
        pets = pets.filter(animal_type=animal_type)
    if breed:
        pets = pets.filter(breed__icontains=breed)
    if gender:
        pets = pets.filter(gender=gender)
    if location:
        pets = pets.filter(location__icontains=location)
    if status:
        pets = pets.filter(status=status)

    return render(request, "pets/pet_list.html", {
        "pets": pets,
        "animal_types": Pet.ANIMAL_TYPES,
        "genders": Pet.GENDERS,
        "statuses": Pet.STATUSES,
    })

def pet_detail(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    return render(request, "pets/pet_detail.html", {"pet": pet})

@login_required
def adoption_create(request, pk):
    pet = get_object_or_404(Pet, pk=pk)
    if pet.status != "Available":
        messages.error(request, "This pet has already been adopted.")
        return redirect("pet_detail", pk=pk)
    if AdoptionRequest.objects.filter(user=request.user, pet=pet, status__in=["Pending", "Approved"]).exists():
        messages.warning(request, "You already have an active request for this pet.")
        return redirect("pet_detail", pk=pk)

    if request.method == "POST":
        form = AdoptionRequestForm(request.POST)
        if form.is_valid():
            adoption = form.save(commit=False)
            adoption.user = request.user
            adoption.pet = pet
            try:
                adoption.save()
            except Exception as exc:
                form.add_error(None, str(exc))
            else:
                messages.success(request, "Adoption application submitted successfully!")
                return redirect("my_adoptions")
    else:
        form = AdoptionRequestForm()
    return render(request, "pets/adoption_form.html", {"form": form, "pet": pet})

@login_required
def my_adoptions(request):
    requests = AdoptionRequest.objects.filter(user=request.user).select_related("pet")
    return render(request, "pets/my_adoptions.html", {"requests": requests})

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("home")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})
