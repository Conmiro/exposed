from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)


class Tag(models.Model):
    title = models.CharField(max_length=32)


class UserTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField()


class Review(models.Model):
    title = models.CharField(max_length=128)
    comment = models.TextField()
    date = models.DateTimeField()


class UploadedImage(models.Model):
    image = models.ImageField(upload_to="images")


class Profile(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    images = models.ManyToManyField(UploadedImage)
    reviews = models.ManyToManyField(Review)
    tags = models.ManyToManyField(UserTag)


