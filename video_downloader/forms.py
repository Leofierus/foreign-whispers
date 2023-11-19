from django import forms


class VideoDownloadForm(forms.Form):
    video_url = forms.URLField(label='Video URL', required=True)
    target_language = forms.ChoiceField(
        label='Target Language',
        choices=[
            ('French', 'French'),
            ('German', 'German'),
        ],
        required=True,
    )
