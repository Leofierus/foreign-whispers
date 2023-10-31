from django import forms


class VideoDownloadForm(forms.Form):
    video_url = forms.URLField()
