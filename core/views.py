import datetime

from PIL import Image
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

# Create your views here.
from core.forms import PhotoForm, NewProfileForm
from core.models import Profile, Location, UploadedImage, Review, Tag, UserTag, StarRating


def home(request):
    return render(request, 'core/home.html')


def browse(request):

    profiles = Profile.objects.all()

    context = {'profiles': profiles}

    return render(request, 'core/browse.html', context)


def handle_image_upload(request):

    file = request.FILES['image']
    image_model = UploadedImage(file=file)
    x = int(float(request.POST.get('x')))
    y = int(float(request.POST.get('y')))
    w = int(float(request.POST.get('width')))
    h = int(float(request.POST.get('height')))

    image = Image.open(file)
    cropped_image = image.crop((x, y, w+x, h+y))
    print(image_model.file.path)
    image_model.save()
    cropped_image.save(image_model.file.path)
    return image_model


def new_profile(request):
    if request.POST:
        new_profile_form = NewProfileForm(request.POST)
        photo_form = PhotoForm(request.POST, request.FILES)
        if photo_form.is_valid() and new_profile_form.is_valid():
            new_prof = new_profile_form.save()
            image = photo_form.save()
            new_prof.images.add(image)
            return redirect('profile', profile_id=new_prof.pk)

    locations = Location.objects.all()
    new_profile_form = NewProfileForm()
    photo_form = PhotoForm()

    context = {'locations': locations, 'photo_form': photo_form, 'new_profile_form': new_profile_form}

    return render(request, 'core/new_profile.html', context)


def profile_view(request, profile_id):

    profile = Profile.objects.get(pk=profile_id)
    now = datetime.datetime.now()

    if request.POST:
        comment = request.POST.get('comment')
        pro_tag = request.POST.get('pro-tag')
        con_tag = request.POST.get('con-tag')
        file = request.FILES.get('file')
        star_rating = request.POST.get('stars')
        if comment:
            title = request.POST.get('comment-title')
            review = Review(title=title, comment=comment, date=now)
            review.save()
            profile.reviews.add(review)
        elif pro_tag:
            try:
                tag = Tag.objects.get(title=pro_tag, isPro=1)
            except ObjectDoesNotExist:
                tag = Tag(title=pro_tag, isPro=1)
                tag.save()

            user_tag = UserTag(tag=tag)
            user_tag.save()
            profile.pro_tags.add(user_tag)
        elif con_tag:
            try:
                tag = Tag.objects.get(title=pro_tag, isPro=0)
            except ObjectDoesNotExist:
                tag = Tag(title=con_tag, isPro=0)
                tag.save()

            user_tag = UserTag(tag=tag)
            user_tag.save()
            profile.con_tags.add(user_tag)
        elif file:
            photo_form = PhotoForm(request.POST, request.FILES)
            if photo_form.is_valid():
                image = photo_form.save()
                profile.images.add(image)
        elif star_rating:
            rating = StarRating(value=star_rating, date=now)
            rating.save()
            profile.star_ratings.add(rating)

    # profile_id = request.POST.get('profile_id')

    total = 0
    count = 0
    for rating in profile.star_ratings.all():
        count += 1
        total += rating.value

    overall_rating = round(total / count, 0) if count else 0

    history = getHistory(profile)
    photo_form = PhotoForm()

    context = {'profile': profile, 'rating': overall_rating, 'history': history, 'photo_form': photo_form}

    return render(request, 'core/profile.html', context)


def getHistory(profile):
    history = []
    for review in profile.reviews.all():
        entry = {'date': review.date, 'comment': "Review Left"}
        history.append(entry)
    for rating in profile.star_ratings.all():
        comment = "Rated "+str(rating.value)+" stars"
        entry = {'date': rating.date, 'comment': comment}
        history.append(entry)

    return sorted(history, key=lambda k: k['date'], reverse=True)

