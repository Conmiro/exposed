from django.db import models


class Location(models.Model):
    city = models.CharField(max_length=32)
    state = models.CharField(max_length=32)

    def __str__(self):
        return self.city+', '+self.state


class Tag(models.Model):
    title = models.CharField(max_length=32)
    isPro = models.BooleanField(default=1)


class UserTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)


class Review(models.Model):
    title = models.CharField(max_length=128)
    comment = models.TextField()
    date = models.DateTimeField()
    vote_count = models.IntegerField(default=0)


class UploadedImage(models.Model):
    file = models.ImageField(upload_to="images")


class StarRating(models.Model):
    value = models.IntegerField(default=3)
    date = models.DateTimeField()


class Profile(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    images = models.ManyToManyField(UploadedImage)
    reviews = models.ManyToManyField(Review)
    pro_tags = models.ManyToManyField(UserTag, related_name="pros")
    con_tags = models.ManyToManyField(UserTag, related_name="cons")
    star_ratings = models.ManyToManyField(StarRating)



