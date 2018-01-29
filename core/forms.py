from PIL import Image
from django import forms

from core.models import UploadedImage


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