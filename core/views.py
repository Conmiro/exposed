from django.shortcuts import render

# Create your views here.
from core.models import Profile, Location, UploadedImage


def home(request):
    return render(request, 'core/home.html')


def browse(request):

    profiles = Profile.objects.all()

    context = {'profiles': profiles}

    return render(request, 'core/browse.html', context)


def new_profile(request):
    if request.POST:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        location = Location.objects.get(pk=request.POST.get('location'))
        file = request.FILES['image']
        new_prof = Profile(
            first_name=first_name,
            last_name=last_name,
            location=location
        )
        new_prof.save()
        image = UploadedImage(image=file)
        image.save()
        new_prof.images.add(image)
        return profile(request, new_prof.pk)

    locations = Location.objects.all()
    context = {'locations': locations}

    return render(request, 'core/new_profile.html', context)


def profile(request, profile_id):

    # profile_id = request.POST.get('profile_id')
    prof = Profile.objects.get(pk=profile_id)

    context = {'profile': prof}


    return render(request, 'core/profile.html', context)


