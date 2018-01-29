from PIL import Image
from django import forms

from core.models import UploadedImage, Profile, Location


class NewProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['location'].empty_label = None  # this removes the default '--------' as first option

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'location')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter last name'})
        }

    def save(self, **kwargs):
        profile = super(NewProfileForm, self).save()
        return profile


class PhotoForm(forms.ModelForm):
    x = forms.FloatField(widget=forms.HiddenInput())
    y = forms.FloatField(widget=forms.HiddenInput())
    width = forms.FloatField(widget=forms.HiddenInput())
    height = forms.FloatField(widget=forms.HiddenInput())
    file = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'}),
        label='Image upload',
        help_text='Please upload a face picture for the profile you are requesting.'
        )

    class Meta:
        model = UploadedImage
        fields = ('file', 'x', 'y', 'width', 'height', )

    def save(self, **kwargs):
        photo = super(PhotoForm, self).save()

        x = self.cleaned_data.get('x')
        y = self.cleaned_data.get('y')
        w = self.cleaned_data.get('width')
        h = self.cleaned_data.get('height')

        image = Image.open(photo.file)
        cropped_image = image.crop((x, y, w+x, h+y))
        resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
        resized_image.save(photo.file.path)

        return photo